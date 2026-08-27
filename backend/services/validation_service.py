class ValidationError(Exception):
    """Raised when the payload structure or data types are invalid."""


class ValidationService:
    """Validates the structure of the received payload.

    Ensures that all the mandatory data exist and matches the correct types.
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
            payload: A dictionary containing the view data and configurations.

        Returns:
            The original payload dictionary if all validations pass.

        Raises:
            ValidationError: If any required field is missing or
            has an invalid type.

        """
        if not isinstance(payload, dict):
            raise ValidationError("Invalid payload.")
        if "idea" not in payload:
            raise ValidationError("The 'idea' field is missing.")
        if "options" not in payload:
            raise ValidationError("The 'options' field is missing.")
        self._validate_idea(payload["idea"])
        self._validate_options(payload["options"])

        return payload

    def _validate_idea(self, idea: dict) -> None:
        if not isinstance(idea, dict):
            raise ValidationError("Invalid idea.")

        if "title" not in idea:
            raise ValidationError("The 'title' field is missing.")
        
        if "description" not in idea:
            raise ValidationError("The 'description' field is missing.")

        if "methodology" not in idea:
            raise ValidationError("The 'methodology' field is missing.")
        self._validate_title(idea["title"])
        self._validate_description(idea["description"])
        self._validate_5w2h(idea["methodology"])

    def _validate_options(self, options: dict) -> None:
        if not isinstance(options, dict):
            raise ValidationError("The options are invalid.")

        if "manual_5w2h" not in options:
            raise ValidationError("The 'manual_5w2h' field is missing.")
        
        if "use_ai" not in options:
            raise ValidationError("The 'use_ai' field is missing.")

        if "show_report" not in options:
            raise ValidationError("The 'show_report' field is missing.")
        self._validate_use_ai(options["use_ai"])

    def _validate_use_ai(self, ai_options) -> None:

        if not isinstance(ai_options, dict):
            raise ValidationError("Invalid AI configuration.")

        if not isinstance(ai_options.get("title"), bool):
            raise ValidationError("Invalid 'title' option.")
        
        methodology = ai_options.get("methodology")

        if not isinstance(methodology, dict):
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

    def _validate_title(self, title) -> None:
        if not isinstance(title, str):
            raise ValidationError("Title must be a text.")
        if not title.strip():
            raise ValidationError("Title can't be empty.")
        if len(title) > 150:
            raise ValidationError("Title must be a maximum of 150 characters long.")

    def _validate_description(self, description) -> None:
        if not isinstance(description, str):
            raise ValidationError("Description must be a text.")
        if not description.strip():
            raise ValidationError("Description can't be empty.")

    def _validate_5w2h(self, methodology) -> None:
        if not isinstance(methodology, dict):
            raise ValidationError("Invalid methodology.")
        if methodology.get("type") != "5w2h":
            raise ValidationError("Invalid methodology type.")
        
        data = methodology.get("data")

        if not isinstance(data, dict):
            raise ValidationError("Invalid 5W2H data.")

        for field in self.REQUIRED_5W2H_FIELDS:

            if field not in data:
                raise ValidationError(
                    f"The '{field}' field is missing in 5W2H."
                )

            value = data[field]

            if not isinstance(value, str):
                raise ValidationError(
                    f"The '{field}' must be text."
                )