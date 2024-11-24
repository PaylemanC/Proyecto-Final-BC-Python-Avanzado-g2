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


def load_congress_data_to_db(
    db_connection,
    congress_df
):
    """
    Load the congress data to the database
    """
    values = [tuple(row) for row in congress_df.values]
    logger.info(f"Loading {len(values)} records to the 'congress' table")
    insert_query = """
        INSERT OR IGNORE INTO congress (congress_id, session, number, start_date, end_date) 
        VALUES(?, ?, ?, ?, ?)
    """
    db_connection.executemany(insert_query, values)
    

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


def load_bills_data_to_db(
    db_connection,
    bills_df
):
    """
    Load the bills data to the database.
    """
    values = [
        (
            row["bill_id"],          
            row["number"],       
            row["type"],         
            row["description"],        
        )
        for _, row in bills_df.iterrows()
    ]

    logger.info(f"Loading {len(values)} bills to the database")

    insert_query = """
        INSERT OR IGNORE INTO bills (bill_id, number, type, description) 
        VALUES (?, ?, ?, ?)
    """
    db_connection.executemany(insert_query, values)
