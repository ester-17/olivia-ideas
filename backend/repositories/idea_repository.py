import json
from backend.database.connection import DatabaseConnection

class IdeaRepositoryError(Exception):
    """
    Raised when an error occurs while persisting idea data.
    """
    pass

class IdeaRepository:
    """
    Handles database persistence for ideas, 5W2H methodology,
    and AI-generated analyses.    """

    def __init__(self):
        self.database = DatabaseConnection()

    # --------------------------------------------------
    # Public methods
    # --------------------------------------------------
    def create(self, idea: dict):
        """
        Persist an idea and its 5W2H data within a single atomic transaction.

        Returns the created idea ID or raises IdeaRepositoryError on failure.
        """
        cursor = self.database.get_cursor()
        try:
            idea_id = self._insert_idea(
                cursor,
                idea
            )
            self._insert_5w2h(
                cursor,
                idea_id,
                idea["methodology"]["data"]
            )
            self.database.commit()
            return idea_id
        
        except Exception as e:
            self.database.rollback()
            raise IdeaRepositoryError(
                f"Failed to create idea: {str(e)}."
                ) from e
        
        finally:
            self.database.close_cursor(cursor)
            self.database.close_connection()

    def save_analysis(self, idea_id: int, analysis: dict) -> None:
        """
        Persists the AI-generated structured analysis for a specific idea.
        """
        cursor = self.database.get_cursor()
        try:
            self._insert_analysis(cursor, idea_id, analysis)

            self.database.commit()

        except Exception as e:
            self.database.rollback()

            raise IdeaRepositoryError(
                f"Failed to save analysis: {str(e)}."
            ) from e

        finally:
            self.database.close_cursor(cursor)
            self.database.close_connection()

    # --------------------------------------------------
    # Private methods
    # --------------------------------------------------

    def _insert_idea(self, cursor, idea: dict) -> int:
        """
        Inserts the main idea record and returns the generated ID.
        """
        sql = """
            INSERT INTO ideas(title, description)
            VALUES(%s, %s)
            """
        values = (
            idea["title"],
            idea["description"],
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

    def _insert_5w2h(self, cursor, idea_id: int, data: dict) -> None:
        """
        Inserts the 5W2H methodology fields linked to the given idea ID.
        """
        sql = """
            INSERT INTO idea_5w2h(
                idea_id, what, why, where_location,
                when_info, who, how, how_much
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """
        values = (
            idea_id,      data["what"],data["why"], data["where"],
            data["when"], data["who"], data["how"], data["how_much"],
        )
        cursor.execute(sql, values)

    def _insert_analysis(self, cursor, idea_id: int, analysis: dict) -> None:
        """
        Serializes and inserts the analysis dictionary as a JSON string.
        """
        sql = """
            INSERT INTO ai_analysis(
                idea_id,
                analysis
            )
            VALUES(%s, %s)
        """
        values = (
            idea_id,
            json.dumps(analysis, ensure_ascii=False)
        )
        cursor.execute(sql, values)