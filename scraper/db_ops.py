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


def load_members_data_to_db(
    db_connection,
    members_df
):
    """
    Load the members data to the database
    """
    values = [tuple(row) for row in members_df.values]
    logger.info(f"Loading {len(values)} members to the database")
    insert_query = """
        INSERT OR IGNORE INTO members (member_id, name, image_url, party_code, state_code) 
        VALUES(?, ?, ?, ?, ?)
    """
    db_connection.executemany(insert_query, values)
