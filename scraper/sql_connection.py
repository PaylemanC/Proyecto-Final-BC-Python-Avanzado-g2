"""
Module for connecting to the database (SQLite)

The DBSession class is a singleton that provides a connection to the database
by instantiating a connection object.
"""
import sqlite3
from loguru import logger
from logger_config import log_level, log_format, log_output


logger.remove()
logger.add(
    log_output, 
    colorize=True, 
    format=log_format,
    level=log_level
)


class DBConnection:
    @staticmethod
    def get_connection():
        DB_PATH = "house_votes_db.sqlite"
        return sqlite3.connect(DB_PATH)
    
    @staticmethod
    def test_connection():
        """
        Test the connection to the database
        
        If the database doesn't exist, it will be created.
        """
        session = DBConnection.get_connection()
        try:
            session.cursor().execute("SELECT 1")
            logger.success("Connection successful")
        except Exception as e:
            logger.exception(f"Connection failed: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    DBConnection.test_connection()
