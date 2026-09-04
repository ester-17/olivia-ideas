import logging
import json
from inspect import cleandoc

logger = logging.getLogger("olivia.services.parser")
class AIResponseParserError(Exception):
    """Raised when the AI response has an invalid structure."""

class AIResponseParser:
    """Parses, validates, and format Ai-generated responses dynamically.

    Handles full analysis payloads as well as partial field processing
    (e.g., title generation or 5W2H refinement).
    """
    
    ANALYSIS_TEXT_FIELDS =(
        "problem",
        "viability",
        "target_audience",
        "risks",
        "competitors",
        "next_steps",
    )

    REQUIRED_5W2H_FIELDS = (
        "what",
        "why",
        "where",
        "when",
        "who",
        "how",
        "how_much",
    )

    def parse(self, text: str) -> dict:
        """Converts the received JSON AI response into a validated dictionary.
        
        Args:
            text: Raw JSON string received from the AI model.

        Return:
            The parsed and validated dictionary.
        """
        data = self._load_json(text)
        self.validate(data)

        return data

    def validate(self, data: dict) -> None:
        """Orchestrates validation of top-level object, title, 5W2H, and analysis fields.
        
        Args:
            data: Parsed dictionary to validate.
            
        Raises:
            AIResponseParserError: If structural or type validation fails.
        """
        logger.debug("Validating AI response")
        if not isinstance(data, dict):
            logger.error("The AI response must be a JSON object.")

            raise AIResponseParserError("The AI response must be a JSON object.")

        # 1. Validate Title (if present in the response)
        if "title" in data and data["title"] is not None:
            logger.debug("Validating title options.")
            if not isinstance(data["title"], str):
                logger.error("Field 'title' must be a string")
                raise AIResponseParserError("Field 'title' must be a string.")
            if not data["title"].strip():
                logger.error("Field 'title' cannot be empty")
                raise AIResponseParserError("Field 'title' cannot be empty.")

        # 2. Validate 5W2H (if present in the response)
        if "fivew2h" in data and data["fivew2h"] is not None:
            logger.debug("Validating 5W2H")
            self._validate_5w2h(data["fivew2h"])

        # 3. Validate Analysis Fields (if analysis object/fields are returned)
        has_any_analysis_field = any(
            field in data for field in self.ANALYSIS_TEXT_FIELDS
        )
        if has_any_analysis_field:
            self._validate_analysis_fields(data)

    def to_markdown(self, analysis: dict) -> str:
        """Converts the analysis dictionary into a formatted Markdown report.
        
        Args:
            analysis: Validated dictionary containing the AI analysis.
            
        Returns:
            A clean, formatted Markdown report string.
        """
        logger.debug("Generating AI report")
        sections = ["# 📊 Relatório da IA"]

        if "problem" in analysis:
            sections.append(self._markdown_problem(analysis))
        if "viability" in analysis:
            sections.append(self._markdown_viability(analysis))
        if "target_audience" in analysis:
            sections.append(self._markdown_target_audience(analysis))
        if "fivew2h" in analysis and analysis["fivew2h"]:
            sections.append(self._markdown_5w2h(analysis))
        if "risks" in analysis:
            sections.append(self._markdown_risks(analysis))
        if "competitors" in analysis:
            sections.append(self._markdown_competitors(analysis))
        if "next_steps" in analysis:
            sections.append(self._markdown_next_steps(analysis))

        return "\n\n---\n\n".join(sections)

    # ==================================================
    # Validation Helpers
    # ==================================================

    def _load_json(self, text: str) -> dict:
        logger.debug("Loading JSON")
        if not text or not text.strip():
            logger.error("The AI response text cannot be empty.")
            raise AIResponseParserError("The AI response text cannot be empty.")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            logger.exception("The AI response is not a valid JSON")
            raise AIResponseParserError(
                "The AI response is not a valid JSON."
                ) from exc

    def _validate_analysis_fields(self, data: dict) -> None:
        """Ensures all expected analysis text fields exist and are non-empty strings."""
        logger.debug("Validating the analysis fields")
        for field in self.ANALYSIS_TEXT_FIELDS:
            if field not in data:
                logger.error(f"Field '{field}' is missing.")
                raise AIResponseParserError(f"Field '{field}' is missing.")

            value = data[field]
            if not isinstance(value, str):
                logger.error(f"Field '{field}' must be a string.")
                raise AIResponseParserError(f"Field '{field}' must be a string.")
            if not value.strip():
                logger.error(f"Field '{field}' cannot be empty.")
                raise AIResponseParserError(f"Field '{field}' cannot be empty.")

    def _validate_5w2h(self, fivew2h: dict) -> None:
        """Validates the 5W2H dictionary structure and value types."""
        if not isinstance(fivew2h, dict):
            raise AIResponseParserError("Field 'fivew2h' must be an object.")

        for field in self.REQUIRED_5W2H_FIELDS:
            if field not in fivew2h:
                raise AIResponseParserError(f"Field '{field}' is missing in 5W2H.")

            value = fivew2h[field]
            if not isinstance(value, str):
                raise AIResponseParserError(f"Field '{field}' in 5W2H must be a string.")
            if not value.strip():
                raise AIResponseParserError(f"Field '{field}' in 5W2H cannot be empty.")


    # ==================================================
    # Markdown Formatting Helpers
    # ==================================================
    logger.debug("Building the markdown")
    def _markdown_problem(self, analysis: dict) -> str:
        return cleandoc( f"""
                ## Problema
                
                {analysis["problem"]}
                """.strip()
        )

    def _markdown_viability(self, analysis: dict) -> str:
        return cleandoc( f"""
                ## Viabilidade
                
                {analysis["viability"]}
            """.strip()
        )

    def _markdown_target_audience(self, analysis: dict) -> str:
        return cleandoc( f"""
                ## Público-alvo
                
                {analysis["target_audience"]}
            """.strip()
        )

    def _markdown_5w2h(self, analysis: dict) -> str:

        fivew2h = analysis["fivew2h"]

        return cleandoc( f"""
                ## 5W2H
                
                ### What (O Quê)
                {fivew2h["what"]}
                
                ### Why (Por Quê)
                {fivew2h["why"]}

                ### Where (Onde)
                {fivew2h["where"]}

                ### When (Quando)
                {fivew2h["when"]}

                ### Who
                {fivew2h["who"]}

                ### How (Como)
                {fivew2h["how"]}

                ### How Much (Quanto)
                {fivew2h["how_much"]}
                """.strip()
        )
    
    def _markdown_risks(self, analysis: dict):
        return cleandoc( f"""
                ## Riscos
                
                {analysis["risks"]}
            """.strip()
        )
    
    def _markdown_competitors(self, analysis: dict):
        return cleandoc( f"""
                ## Concorrentes
                
                {analysis["competitors"]}
            """.strip()
        )

    def _markdown_next_steps(self, analysis: dict):
        return cleandoc( f"""
                ## Próximos Passos
                
                {analysis["next_steps"]}
            """.strip()
        )