import logging
from google import genai
import os
from dotenv import load_dotenv

from backend.services.ai_response_parser import AIResponseParser
from backend.services.prompt_service import PromptService

logger = logging.getLogger("olivia.services.ai")
load_dotenv()

class AIServiceError(Exception):
    """
    Raised when the AI communication fails.
    """
    pass

class AIService:
    """
    Manages all interactions with the Gemini AI service.

    Attributes:
        prompt_service: Service responsible for building the prompt structure.
        parser: Service responsible for parsing and formatting the AI response.
        client: The initialized Google GenAI client instance.
    """

    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self) -> None:
        logger.debug("Initializing AIService")

        self.prompt_service = PromptService()
        self.parser = AIResponseParser()
        self.client = self._create_client()

    def generate(self, payload: dict) -> dict:
        """
        Generates an idea analysis using the AI model.

        Args:
            payload: A dictionary containing validated data from ValidationService.

        Returns:
            The parsed Python object processed by the AIResponseParser.
        """ 
        logger.info("Starting idea analysis")

        prompt = self._build_prompt(payload)
        response = self._call_model(prompt)
        text = self._extract_text(response)

        analysis = self.parser.parse(text)
        logger.debug("AI response parsed successfully")

        return analysis

    def to_markdown(self, analysis) -> str:
        """
        Converts the parsed analysis object into Markdown format.

        Args:
            analysis: The parsed Python object containing the AI analysis.
            
        Returns:
            A string containing the formatted Markdown report.
        """
        return self.parser.to_markdown(analysis)


    def _build_prompt(self, payload: dict) -> str:
        """
        Builds the prompts to be sent to Gemini.

        Args:
            payload: validated data containing the idea and its methodology.

        Returns:
            The complete prompt text.
        """
        logger.debug("Building prompt for AI model")

        return self.prompt_service.build(payload)

    def _call_model(self, prompt: str):
        """
        Sends a prompt to Gemini model.

        Args:
            prompt: The text prompt to be processed by the model.

        Returns:
            The raw response returned by the Google GenAI SDK.

        Raises:
            AIServiceError: if the API call fails.
        """
        try:
            logger.debug("Calling Gemini model | model=%s", self.MODEL_NAME)
            return self.client.models.generate_content(
                model=self.MODEL_NAME,
                contents=prompt
            )
        except Exception as exc:
            logger.exception("Failed to communicate with Gemini")
            raise AIServiceError("Failed to communicate with Gemini.") from exc

    def _extract_text(self, response) -> str:
        """
        Extracts and validates the text from Gemini response.

        Args:
            response: Raw response returned by the Google GenAI SDK.

        Returns:
            The cleaned text returned by the model.

        Raises:
            AIServiceError: If the response is missing, invalid, or empty.
        """
        if response is None:
            logger.error("No response returned from Gemini")
            raise AIServiceError(
                "Nenhuma resposta foi retornada pela IA."
            )

        if not hasattr(response, "text"):
            logger.error("Invalid response structure from Gemini")
            raise AIServiceError(
                "Resposta inválida recebida da IA."
            )

        if not response.text:
            logger.error("Empty response text from Gemini")
            raise AIServiceError(
                "A IA retornou uma resposta vazia."
            )

        return response.text.strip()

    def _create_client(self) -> genai.Client:
        """
        Creates and configures the Google GenAI client.

        Returns:
            An initialized Google GenAI client.
        """
        logger.debug("Creating Google GenAI client")
        api_key = self._get_api_key()

        return genai.Client(api_key=api_key)

    def _get_api_key(self) -> str:
        """
        Fetches the Gemini API key from the environment variables.

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