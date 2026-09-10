import logging
import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

from backend.services.ai_response_parser import AIResponseParser
from backend.services.prompt_service import PromptService

logger = logging.getLogger("olivia.services.ai")
load_dotenv()

class AIServiceError(Exception):
    """Raised when the AI communication, generation, or parsing fails."""
    pass

class AIService:
    """Manages all interactions with the Gemini AI service.

    Attributes:
        prompt_service: Service responsible for building dynamic prompt structures.
        parser: Service responsible for parsing and formatting the AI response.
        client: The initialized Google GenAI client instance.
    """

    PRIMARY_MODEL = "gemini-3.6-flash"
    FALLBACK_MODEL = "gemini-2.5-flash"

    def __init__(self) -> None:
        """Initializes the AIService with prompt builder,
        response parser, and api client."""
        logger.debug("Initializing AIService")

        self.prompt_service = PromptService()
        self.parser = AIResponseParser()
        self.client = self._create_client()

    def process(self, payload: dict, ai_tasks: dict) -> tuple[dict, dict | None]:
        """Executes all requested AI tasks and analysis in a single Ai call.

        Args:
            payload:Validated idea payload.
            ai_tasks: Dictionary containing resolved AI tasks.

        Returns:
            A tuple containing:
                - The updated payload with AI generated title and/or 5W2H fields.
                - The parsed analysis dictionary if requested, otherwise None.

        Raises:
            AIServiceError: If prompt creation, model execution, or parsing fails.
        """ 
        logger.info("Processing single-pass AI tasks | tasks=%s", ai_tasks)

        # 1. Build unified prompt
        prompt = self.prompt_service.build(payload, ai_tasks)

        # 2. Call Gemini model
        response = self._call_model(prompt)
        text = self._extract_text(response)

        # 3. Parse JSON response
        logger.debug("Raw AI response | text=%r", text)
        parsed_response = self.parser.parse(text)
        logger.debug("AI response parsed successfully")

        # 4. Update payload with generated/refined fields
        if "title" in ai_tasks and "title" in parsed_response:
            payload["idea"]["title"] = parsed_response["title"]
            logger.debug("Updated payload title from AI response")

        if "methodology" in ai_tasks and "fivew2h" in parsed_response:
            payload["idea"]["methodology"]["data"].update(parsed_response["fivew2h"])
            logger.debug("Updated payload 5W2H methodology from AI response")

        # 5. Extract internal analysis payload if requested
        analysis_data = parsed_response.get(
            "analysis"
        ) if ai_tasks.get("analysis") else None

        return payload, analysis_data

    def to_markdown(self, analysis) -> str:
        """Converts the parsed analysis object into Markdown format.

        Args:
            analysis: The parsed Python object containing the AI analysis.
            
        Returns:
            A string containing the formatted Markdown report.
        """
        return self.parser.to_markdown(analysis)

    def _call_model(self, prompt: str):
        """Sends a prompt to Gemini model.

        Args:
            prompt: The text prompt to be processed by the model.

        Returns:
            The raw response returned by the Google GenAI SDK.

        Raises:
            AIServiceError: if the API call fails.
        """
        models_to_try = [self.PRIMARY_MODEL, self.FALLBACK_MODEL]

        for index, model in enumerate(models_to_try):
            try:
                logger.debug("Calling Gemini model | model=%s", model)
                return self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
            except errors.APIError as err:
                logger.warning(
                    "Gemini API error | model=%s | status=%s | message=%s",
                    model,
                    err.code,
                    err.message,
                )
                is_last_model = (index == len(models_to_try)-1)

                if err.code in (503, 429) and not is_last_model:
                    logger.info("Retrying request with next fallback model...")
                    continue

                raise AIServiceError(
                    "Gemini API request failed."
                    ) from None
            
            except Exception as exc:
                logger.exception(
                    "Unexpected error communicating with Gemini | model=%s", model)
                raise AIServiceError(
                    "Unexpected error while communicating with Gemini."
            ) from None

        raise AIServiceError(
            "All configured Gemini models failed."
        )

    def _extract_text(self, response) -> str:
        """Extracts and validates the text from Gemini response.

        Args:
            response: Raw response returned by the Google GenAI SDK.

        Returns:
            The cleaned text returned by the model.

        Raises:
            AIServiceError: If the response is missing, invalid, or empty.
        """
        if response is None:
            logger.error("No response returned from Gemini")
            raise AIServiceError("Nenhuma resposta foi retornada pela IA.")

        if not hasattr(response, "text"):
            logger.error("Invalid response structure from Gemini")
            raise AIServiceError("Resposta inválida recebida da IA.")

        if not response.text:
            logger.error("Empty response text from Gemini")
            raise AIServiceError(
                "A IA retornou uma resposta vazia."
            )

        return response.text.strip()

    def _create_client(self) -> genai.Client:
        """Creates and configures the Google GenAI client.

        Returns:
            An initialized Google GenAI client.
        """
        logger.debug("Creating Google GenAI client")
        api_key = self._get_api_key()

        return genai.Client(api_key=api_key)

    def _get_api_key(self) -> str:
        """Fetches the Gemini API key from the environment variables.

        Returns:
            The API key string.

        Raises:
            AIServiceError: If the GEMINI_API_KEY is not defined.
        """
        logger.debug("Fetching Gemini API key")
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise AIServiceError("GEMINI_API_KEY not found")

        return key