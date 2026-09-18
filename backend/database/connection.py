"""MySQL connection and transaction management."""

import os
from typing import Any

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


class DatabaseConnectionError(Exception):
    """Raised when a MySQL connection cannot be created."""


class DatabaseConnection:
    """Manage a MySQL connection, cursors, and transactions.

    Attributes:
        _connection: Lazily created MySQL connection, when available.
    """

    def __init__(self) -> None:
        """Initialize the connection manager without opening a connection."""
        self._connection: Any | None = None

    def create_connection(self) -> Any:
        """Create and return the active MySQL connection.

        Returns:
            A connection created by ``mysql.connector``.

        Raises:
            DatabaseConnectionError: If MySQL rejects or cannot establish the connection.
        """
        if self._connection is None:
            try:
                self._connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=int(os.getenv("DB_PORT", "3306")),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                )
            except (ValueError, mysql.connector.Error) as exc:
                raise DatabaseConnectionError("Could not connect to the database.") from exc
        return self._connection

    def get_cursor(self) -> Any:
        """Return a dictionary cursor for the active connection.

        Returns:
            A MySQL cursor configured to return dictionaries.
        """
        return self.create_connection().cursor(dictionary=True)

    def close_cursor(self, cursor: Any | None) -> None:
        """Close a cursor when one was created.

        Args:
            cursor: The cursor to close, or ``None``.
        """
        if cursor is not None:
            cursor.close()

    def commit(self) -> None:
        """Commit the active transaction, if a connection exists."""
        if self._connection is not None:
            self._connection.commit()

    def rollback(self) -> None:
        """Roll back the active transaction, if a connection exists."""
        if self._connection is not None:
            self._connection.rollback()

    def close_connection(self) -> None:
        """Close and discard the active database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
