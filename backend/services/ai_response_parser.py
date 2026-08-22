import json

class AIResponseParserError(Exception):
    """Raised when the AI response has an invalid structure."""

class AIResponseParser:
    """Parses, validates, and formats AI-generated analysis responses.

    The parser converts JSON responses into Python dictionaries, validates their
    structure and data types, and formats validated data as Markdown.

    Attributes:
        REQUIRED_FIELDS: A tuple containing all mandatory top-level fields.
        REQUIRED_5W2H_FIELDS: A tuple containing the mandatory fields
        inside the 5W2H section.
        TEXT_FIELDS: A tuple of required text fields excluding 5W2H.
    """

    
    REQUIRED_FIELDS =(
        "problem",
        "viability",
        "target_audience",
        "fivew2h",
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

    TEXT_FIELDS = (
        "problem",
        "viability",
        "target_audience",
        "risks",
        "competitors",
        "next_steps",
    )

    def parse(self, text: str) -> dict:
        """Converts the received JSON AI response into a Python object.
        
        Args:
            text: Raw JSON string received from the AI model.

        Return:
            The parsed and validated dictionary.
        """
        data = self._load_json(text)
        self.validate(data)

        return data

    def validate(self, data: dict):
        """Orchestrates the validation process of different received fields.
        
        Args:
            data: The parsed dictionary to be validated.
            
        Raises:
            AIResponseParserError: If any structural or type validation fails."""
        self._validate_structure(data)
        self._validate_types(data)
        self._validate_5w2h(data["fivew2h"])

    def to_markdown(self, analysis: dict) -> str:
        """Converts the received Python object into Markdown.
        
        Args:
            analysis: The validated dictionary containing the AI analysis.
            
        Returns:
            A clean, formatted Markdown string report."""
        sections = [
            "# 📊 Relatório da IA",

            self._markdown_problem(analysis),
            self._markdown_viability(analysis),
            self._markdown_target_audience(analysis),
            self._markdown_5w2h(analysis),
            self._markdown_risks(analysis),
            self._markdown_competitors(analysis),
            self._markdown_next_steps(analysis),
        ]

        return "\n\n---\n\n".join(sections)

    def _load_json(self, text: str):
        if not text:
            raise AIResponseParserError("The AI response text cannot be empty.")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise AIResponseParserError(
                "The AI response is not a valid JSON."
                ) from exc

    def _validate_structure(self, data: dict):
        if not isinstance(data, dict):
            raise AIResponseParserError(
                "The AI response must be an object."
            )

        for field in self.REQUIRED_FIELDS:

            if field not in data:

                raise AIResponseParserError(
                    f"The '{field}' field is missing."
                )

            if data[field] is None:
                raise AIResponseParserError(
                    f"The '{field}' field is empty."
                )

    def _validate_types(self, data: dict) -> None:

        for field in self.TEXT_FIELDS:
            value = data[field]
            if not isinstance(value, str):
                raise AIResponseParserError(
                    f"The '{field}' field must be a string."
                )

            if not value.strip():
                raise AIResponseParserError(
                    f"The '{field}' field cannot be empty."
                )
    def _validate_5w2h(self, fivew2h: dict) -> None:
        if not isinstance(fivew2h, dict):
            raise AIResponseParserError(
                "5W2H must be an object."
            )
        for field in self.REQUIRED_5W2H_FIELDS:
            if field not in fivew2h:
                raise AIResponseParserError(
                    f"Field '{field}' is missing."
                )

            value = fivew2h[field]

            if not isinstance(value, str):
                raise AIResponseParserError(
                    f"Field '{field}' must be a string."
                )

            if not value.strip():
                raise AIResponseParserError(
                    f"Field '{field}' cannot be empty."
                )
            
    def _markdown_problem(self, analysis: dict):
        return f"""
                ## Problema
                
                {analysis["problem"]}
                """.strip()

    def _markdown_viability(self, analysis: dict):
        return f"""
                ## Viabilidade
                
                {analysis["viability"]}
            """.strip()

    def _markdown_target_audience(self, analysis: dict):
        return f"""
                ## Público-alvo
                
                {analysis["target_audience"]}
            """.strip()

    def _markdown_5w2h(self, analysis: dict):

        fivew2h = analysis["fivew2h"]

        return f"""
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
    
    def _markdown_risks(self, analysis: dict):
        return f"""
                ## Riscos
                
                {analysis["risks"]}
            """.strip()
    
    def _markdown_competitors(self, analysis: dict):
        return f"""
                ## Concorrentes
                
                {analysis["competitors"]}
            """.strip()

    def _markdown_next_steps(self, analysis: dict):
        return f"""
                ## Próximos Passos
                
                {analysis["next_steps"]}
            """.strip()