import json
import logging
from inspect import cleandoc

logger = logging.getLogger("olivia.services.parser")


class AIResponseParserError(Exception):
    """Raised when the AI response has an invalid structure or data type."""

    pass


class AIResponseParser:
    """Parses, validates, and formats AI-generated responses dynamically.

    Handles full analysis payloads as well as partial field processing
    (e.g., title generation or 5W2H refinement).
    """

    REQUIRED_5W2H_FIELDS = (
        "what",
        "why",
        "where",
        "when",
        "who",
        "how",
        "how_much",
    )

    ANALYSIS_SCHEMA = {
        "problem": str,
        "viability": int,
        "target_audience": str,
        "risks": list,
        "competitors": list,
        "next_steps": list,
    }

    def parse(self, text: str) -> dict:
        """Converts the received JSON AI response into a validated dictionary.

        Args:
            text: Raw JSON string received from the AI model.

        Returns:
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
        logger.debug("Validating AI response structure")

        if not isinstance(data, dict):
            logger.error("The AI response must be a JSON object.")
            raise AIResponseParserError("The AI response must be a JSON object.")

        # 1. Validate Title (if present in the response)
        if "title" in data and data["title"] is not None:
            logger.debug("Validating title field")
            if not isinstance(data["title"], str):
                logger.error("Field 'title' must be a string.")
                raise AIResponseParserError("Field 'title' must be a string.")
            if not data["title"].strip():
                logger.error("Field 'title' cannot be empty.")
                raise AIResponseParserError("Field 'title' cannot be empty.")

        # 2. Validate 5W2H (if present in the response)
        if "fivew2h" in data and data["fivew2h"] is not None:
            logger.debug("Validating 5W2H fields")
            self._validate_5w2h(data["fivew2h"])

        # 3. Validate Analysis Object (if present in the response)
        if "analysis" in data and data["analysis"] is not None:
            logger.debug("Validating analysis object")
            self._validate_analysis(data["analysis"])

    def to_markdown(self, analysis: dict) -> str:
        """Converts the analysis dictionary into a formatted Markdown report.

        Args:
            analysis: Validated dictionary containing the AI analysis object.

        Returns:
            A clean, formatted Markdown report string.
        """
        logger.debug("Generating AI report in Markdown format")
        if not isinstance(analysis,dict):
            logger.error(
                "Analysis payload must be a dictionary to convert to markdown"
            )
            raise AIResponseParserError("Analysis payload must be a dictionary.")
        
        sections = ["# 📊 Relatório da IA"]

        if "problem" in analysis:
            sections.append(self._markdown_problem(analysis))
        if "viability" in analysis:
            sections.append(self._markdown_viability(analysis))
        if "target_audience" in analysis:
            sections.append(self._markdown_target_audience(analysis))
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
        logger.debug("Loading and cleaning JSON response")

        if not text or not text.strip():
            logger.error("The AI response text cannot be empty.")
            raise AIResponseParserError("The AI response text cannot be empty.")

        cleaned_text = text.strip()
        if cleaned_text.startswith("```"):
            lines = cleaned_text.splitlines()
            if lines[0].strip().lower() in ("```json", "```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned_text = "\n".join(lines).strip()

        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            logger.exception("The AI response is not a valid JSON")
            raise AIResponseParserError(
                "The AI response is not a valid JSON."
            ) from exc

    def _validate_analysis(self, analysis: dict) -> None:
        """Validates structure, types, and constraints for the 'analysis' object."""
        if not isinstance(analysis, dict):
            logger.error("Field 'analysis' must be an object.")
            raise AIResponseParserError("Field 'analysis' must be an object.")

        for field, expected_type in self.ANALYSIS_SCHEMA.items():
            if field not in analysis:
                logger.error(f"Field '{field}' is missing in analysis.")
                raise AIResponseParserError(f"Field '{field}' is missing in analysis.")

            value = analysis[field]

            # Prevent boolean values from passing as integers (bool is a subclass of int in Python)
            if expected_type is int and isinstance(value, bool):
                logger.error(f"Field '{field}' in analysis must be an integer, not a boolean.")
                raise AIResponseParserError(f"Field '{field}' in analysis must be an integer, not a boolean.")

            if not isinstance(value, expected_type):
                logger.error(f"Field '{field}' in analysis must be of type {expected_type.__name__}.")
                raise AIResponseParserError(
                    f"Field '{field}' in analysis must be of type {expected_type.__name__}."
                )

            # Specific constraints
            if expected_type is str and not value.strip():
                logger.error(f"Field '{field}' in analysis cannot be empty.")
                raise AIResponseParserError(f"Field '{field}' in analysis cannot be empty.")

            if expected_type is int and not (0 <= value <= 100):
                logger.error(f"Field '{field}' in analysis must be between 0 and 100.")
                raise AIResponseParserError(f"Field '{field}' in analysis must be between 0 and 100.")

            if expected_type is list:
                if not value:
                    logger.error(f"Field '{field}' in analysis cannot be an empty list.")
                    raise AIResponseParserError(f"Field '{field}' in analysis cannot be an empty list.")
                for item in value:
                    if not isinstance(item, str) or not item.strip():
                        logger.error(f"All items in '{field}' list in analysis must be non-empty strings.")
                        raise AIResponseParserError(
                            f"All items in '{field}' list in analysis must be non-empty strings."
                        )

    def _validate_5w2h(self, fivew2h: dict) -> None:
        """Validates the 5W2H dictionary structure and value types."""
        if not isinstance(fivew2h, dict):
            logger.error("Field 'fivew2h' must be an object.")
            raise AIResponseParserError("Field 'fivew2h' must be an object.")

        for field in self.REQUIRED_5W2H_FIELDS:
            if field not in fivew2h:
                logger.error(f"Field '{field}' is missing in 5W2H.")
                raise AIResponseParserError(f"Field '{field}' is missing in 5W2H.")

            value = fivew2h[field]
            if not isinstance(value, str):
                logger.error(f"Field '{field}' in 5W2H must be a string.")
                raise AIResponseParserError(f"Field '{field}' in 5W2H must be a string.")
            if not value.strip():
                logger.error(f"Field '{field}' in 5W2H cannot be empty.")
                raise AIResponseParserError(f"Field '{field}' in 5W2H cannot be empty.")

    # ==================================================
    # Markdown Formatting Helpers
    # ==================================================

    def _markdown_problem(self, analysis: dict) -> str:
        return cleandoc(f"""
            ## Problema

            {analysis['problem']}
        """)

    def _markdown_viability(self, analysis: dict) -> str:
        return cleandoc(f"""
            ## Viabilidade

            **Pontuação:** {analysis['viability']}/100
        """)

    def _markdown_target_audience(self, analysis: dict) -> str:
        return cleandoc(f"""
            ## Público-alvo

            {analysis['target_audience']}
        """)

    def _markdown_risks(self, analysis: dict) -> str:
        items = "\n".join(f"- {risk}" for risk in analysis["risks"])
        return cleandoc(f"""
            ## Riscos

            {items}
        """)

    def _markdown_competitors(self, analysis: dict) -> str:
        items = "\n".join(f"- {competitor}" for competitor in analysis["competitors"])
        return cleandoc(f"""
            ## Concorrentes

            {items}
        """)

    def _markdown_next_steps(self, analysis: dict) -> str:
        items = "\n".join(f"- {step}" for step in analysis["next_steps"])
        return cleandoc(f"""
            ## Próximos Passos

            {items}
        """)