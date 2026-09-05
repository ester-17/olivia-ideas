import logging

logger = logging.getLogger("olivia.services.validation")


class ValidationError(Exception):
    """Raised when the payload structure or data types are invalid."""


class ValidationService:
    """Validates the structure of the received payload.

    Ensures that all mandatory data exists and matches the correct types.
    Does not apply any business logic.

    Attributes:
        REQUIRED_5W2H_FIELDS: A tuple containing the mandatory fields for 5W2H.
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

    def validate_payload(self, payload: dict) -> dict:
        """Validates the entire incoming payload structure.

        Args:
            payload: A dictionary containing the idea data and options.

        Returns:
            The original payload dictionary if all validations pass.

        Raises:
            ValidationError: If any required field is missing or
            has an invalid type.
        """
        logger.debug("Validating payload structure and data types")

        if not isinstance(payload, dict):
            logger.error("Invalid payload.")
            raise ValidationError("Invalid payload.")

        if "idea" not in payload:
            logger.error("The 'idea' field is missing in the payload.")
            raise ValidationError("The 'idea' field is missing.")

        if "options" not in payload:
            logger.error("The 'options' field is missing in the payload.")
            raise ValidationError("The 'options' field is missing.")

        # Validate options first because _validate_idea
        # depends on the AI configuration.
        self._validate_options(payload["options"])

        self._validate_idea(
            payload["idea"],
            payload["options"]["ai_options"]
        )

        return payload

    def _validate_idea(self, idea: dict, ai_options: dict) -> None:
        """Validate the idea data."""

        logger.debug("Validating idea")

        if not isinstance(idea, dict):
            logger.error("Invalid idea.")
            raise ValidationError("Invalid idea.")

        if "title" not in idea:
            logger.error("The 'title' field is missing.")
            raise ValidationError("The 'title' field is missing.")

        if "description" not in idea:
            logger.error("The 'description' field is missing.")
            raise ValidationError("The 'description' field is missing.")

        if "methodology" not in idea:
            logger.error("The 'methodology' field is missing.")
            raise ValidationError("The 'methodology' field is missing.")

        self._validate_title(
            idea["title"],
            ai_options
        )

        self._validate_description(
            idea["description"]
        )

        self._validate_5w2h(
            idea["methodology"]
        )

    def _validate_options(self, options: dict) -> None:
        """Validate processing and AI options."""

        logger.debug("Validating options")

        if not isinstance(options, dict):
            logger.error("Invalid options.")
            raise ValidationError("The options are invalid.")

        if "manual_5w2h" not in options:
            logger.error("The 'manual_5w2h' field is missing.")
            raise ValidationError("The 'manual_5w2h' field is missing.")

        if "generate_analysis" not in options:
            logger.error("The 'generate_analysis' field is missing.")
            raise ValidationError("The 'generate_analysis' field is missing.")

        if "show_report" not in options:
            logger.error("The 'show_report' field is missing.")
            raise ValidationError("The 'show_report' field is missing.")

        if "ai_options" not in options:
            logger.error("The 'ai_options' field is missing.")
            raise ValidationError("The 'ai_options' field is missing.")

        self._validate_use_ai(
            options["ai_options"]
        )

    def _validate_use_ai(self, ai_options: dict) -> None:
        """Validate AI configuration."""

        if not isinstance(ai_options, dict):
            logger.error("Invalid AI options/configuration.")
            raise ValidationError("Invalid AI configuration.")

        if not isinstance(ai_options.get("title"), bool):
            logger.error("Invalid 'title' option.")
            raise ValidationError("Invalid 'title' option.")

        methodology = ai_options.get("methodology")

        if not isinstance(methodology, dict):
            logger.error("Invalid 5W2H configuration.")
            raise ValidationError("Invalid 5W2H configuration.")

        for field in self.REQUIRED_5W2H_FIELDS:

            if field not in methodology:
                raise ValidationError(
                    f"Missing AI option for '{field}'."
                )

            if not isinstance(methodology[field], bool):
                raise ValidationError(
                    f"The option '{field}' must be boolean."
                )

    def _validate_title(self, title: str, ai_options: dict) -> None:
        """Validate the idea title."""

        if not isinstance(title, str):
            logger.error("Title must be a text.")
            raise ValidationError("Title must be a text.")

        if not title.strip() and not ai_options.get("title", False):
            logger.error("Title can't be empty without AI option.")
            raise ValidationError(
                "Title can't be empty without AI option."
            )

    def _validate_description(self, description: str) -> None:
        """Validate the idea description."""

        if not isinstance(description, str):
            logger.error("Description must be a text.")
            raise ValidationError("Description must be a text.")

        if not description.strip():
            logger.error("Description can't be empty.")
            raise ValidationError("Description can't be empty.")

    def _validate_5w2h(self, methodology: dict) -> None:
        """Validate the 5W2H methodology."""

        if not isinstance(methodology, dict):
            logger.error("Invalid methodology.")
            raise ValidationError("Invalid methodology.")

        if methodology.get("type") != "5w2h":
            logger.error("Invalid methodology type.")
            raise ValidationError("Invalid methodology type.")

        data = methodology.get("data")

        if not isinstance(data, dict):
            logger.error("Invalid 5W2H data type.")
            raise ValidationError("Invalid 5W2H data.")

        for field in self.REQUIRED_5W2H_FIELDS:

            if field not in data:
                logger.error(
                    "The '%s' field is missing in 5W2H.",
                    field
                )

                raise ValidationError(
                    f"The '{field}' field is missing in 5W2H."
                )

            value = data[field]

            if not isinstance(value, str):
                logger.error(
                    "The '%s' must be text.",
                    field
                )

                raise ValidationError(
                    f"The '{field}' must be text."
                )