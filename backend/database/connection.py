import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnectionError(Exception):
    """
    Raised when a database connection fails.
    """
    pass

class DatabaseConnection:
    """
    Manages the lifecycle of a database connection and its transactions.

    This class provides methods to open and close connections, manage
    database cursors, and commit or rollback active transactions.
    """

    def __init__(self) -> None:
        self._connection: mysql.connector.MySQLConnection | None = None

    def create_connection(self) -> "mysql.connector.MySQLConnection":
        """
        Creates a connection to MySQL if it does not already exist.

        Returns:
            The active MySQL connection object.
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
            except mysql.connector.Error as exc:
                raise DatabaseConnectionError(
                    "Could not connect to the database."
                ) from exc

        return self._connection
    
    def get_cursor(self) -> mysql.connector.cursor.MySQLCursor:
        """
        Returns a cursor for executing SQL commands.
        """
        connection = self.create_connection()
        return connection.cursor(dictionary=True)

    def close_cursor(self, cursor: mysql.connector.cursor.MySQLCursor | None) -> None:
        """
        Closes an active database cursor.
        
        Args:
            cursor: The MySQL cursor object to be closed.
        """
        if cursor is not None:
            cursor.close()

    def commit(self) -> None:
        """
        Commits the current transaction to the database.
        """
        if self._connection is not None:
            self._connection.commit()

    def rollback(self) -> None:
        """
        Rollbacks the current transaction to the database.
        """
        if self._connection is not None:
            self._connection.rollback()

    def close_connection(self) -> None:
        """
        Closes the active database connection safely.
        """
        if self._connection:
            self._connection.close()
            self._connection = None
