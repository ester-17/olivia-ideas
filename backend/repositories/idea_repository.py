"""Persistence operations for ideas and AI analyses."""

import json
from typing import Any, Mapping

from backend.database.connection import DatabaseConnection


class IdeaRepositoryError(Exception):
    """Raised when an idea or its analysis cannot be persisted."""


class IdeaRepository:
    """Persist ideas, their 5W2H data, and generated analyses.

    Attributes:
        database: Connection manager used by repository operations.
    """

    METHODOLOGY_FIELDS = (
        "what",
        "why",
        "where",
        "when",
        "who",
        "how",
        "how_much",
    )
    ALLOWED_SOURCES = frozenset({"USER", "AI"})

    def __init__(self, database: DatabaseConnection | None = None) -> None:
        """Initialize the repository.

        Args:
            database: Optional connection manager, primarily for dependency injection.
        """
        self.database = database or DatabaseConnection()

    def create(self, idea: Mapping[str, Any]) -> int:
        """Persist an idea and its 5W2H information atomically.

        Args:
            idea: Validated idea data containing title, description, and methodology.

        Returns:
            The generated idea identifier.

        Raises:
            IdeaRepositoryError: If any insert or transaction operation fails.
        """
        cursor = self.database.get_cursor()
        try:
            idea_id = self._insert_idea(cursor, idea)
            methodology = idea["methodology"]
            self._insert_5w2h(
                cursor,
                idea_id,
                methodology["data"],
                methodology["sources"],
            )
            self.database.commit()
            return idea_id
        except Exception as exc:
            self.database.rollback()
            raise IdeaRepositoryError("Failed to create idea.") from exc
        finally:
            self.database.close_cursor(cursor)
            self.database.close_connection()

    def save_analysis(self, idea_id: int, analysis: Mapping[str, Any]) -> None:
        """Persist a structured AI analysis for an idea.

        Args:
            idea_id: Identifier of the persisted idea.
            analysis: Analysis containing a numeric score and JSON-serializable details.

        Raises:
            IdeaRepositoryError: If the analysis cannot be saved.
        """
        cursor = self.database.get_cursor()
        try:
            self._insert_analysis(cursor, idea_id, analysis)
            self.database.commit()
        except Exception as exc:
            self.database.rollback()
            raise IdeaRepositoryError("Failed to save analysis.") from exc
        finally:
            self.database.close_cursor(cursor)
            self.database.close_connection()

    def _insert_idea(self, cursor: Any, idea: Mapping[str, Any]) -> int:
        """Insert the primary idea record.

        Args:
            cursor: Cursor used to execute the statement.
            idea: Validated idea data.

        Returns:
            The generated identifier.
        """
        cursor.execute(
            "INSERT INTO ideas (title, description) VALUES (%s, %s)",
            (idea["title"], idea["description"]),
        )
        return int(cursor.lastrowid)

    def _insert_5w2h(
        self,
        cursor: Any,
        idea_id: int,
        data: Mapping[str, str],
        sources: Mapping[str, str],
    ) -> None:
        """Insert methodology data associated with an idea.

        Args:
            cursor: Cursor used to execute the statement.
            idea_id: Identifier of the idea.
            data: Validated 5W2H values.
            sources: Origin for each value. A manually preserved value is ``USER``;
                any value generated or refined by AI is ``AI``.

        Raises:
            IdeaRepositoryError: If a source is not exactly ``USER`` or ``AI``.
        """
        validated_sources = self._validate_sources(sources)
        cursor.execute(
            """INSERT INTO idea_5w2h
            (idea_id, what, what_source, why, why_source, where_location,
             where_location_source, when_info, when_source, who, who_source,
             how, how_source, how_much, how_much_source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                idea_id,
                data["what"], validated_sources["what"],
                data["why"], validated_sources["why"],
                data["where"], validated_sources["where"],
                data["when"], validated_sources["when"],
                data["who"], validated_sources["who"],
                data["how"], validated_sources["how"],
                data["how_much"], validated_sources["how_much"],
            ),
        )

    def _validate_sources(self, sources: Mapping[str, str]) -> dict[str, str]:
        """Validate and normalize 5W2H source values before persistence.

        A field keeps ``USER`` only when no AI operation changed it. Generated and
        refined values use ``AI``; ``USER_EDITED_AI`` is intentionally unsupported.

        Args:
            sources: Source values keyed by the canonical 5W2H field names.

        Returns:
            A complete mapping containing only ``USER`` or ``AI``.

        Raises:
            IdeaRepositoryError: If a field is missing or has an unsupported source.
        """
        invalid_fields = [
            field
            for field in self.METHODOLOGY_FIELDS
            if sources.get(field) not in self.ALLOWED_SOURCES
        ]
        if invalid_fields:
            raise IdeaRepositoryError(
                "Invalid 5W2H source for fields: " + ", ".join(invalid_fields)
            )
        return {field: sources[field] for field in self.METHODOLOGY_FIELDS}

    def _insert_analysis(self, cursor: Any, idea_id: int, analysis: Mapping[str, Any]) -> None:
        """Insert a JSON-serialized analysis.

        Args:
            cursor: Cursor used to execute the statement.
            idea_id: Identifier of the idea.
            analysis: Storage-ready analysis data.
        """
        cursor.execute(
            "INSERT INTO ai_analysis (idea_id, score, analysis_data) VALUES (%s, %s, %s)",
            (idea_id, analysis["score"], json.dumps(analysis["analysis_data"], ensure_ascii=False)),
        )
