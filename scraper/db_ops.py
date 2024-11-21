from loguru import logger
from logger_config import log_level, log_format, log_output


logger.remove()
logger.add(
    log_output, 
    colorize=True, 
    format=log_format,
    level=log_level
)


def initiliaze_db(
    db_connection,
    sql_file_path: str
):
    """
    Initialize the database with the schema
    and values from the main sql file
    """
    with open(sql_file_path, "r") as file:
        db_connection.executescript(file.read())
