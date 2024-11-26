"""
Main entry point for the application to load data into the database.

Responsibilities:
- Establishes a database connection using the `DBConnection` class.
- Optionally sets up the database schema by executing SQL from the provided schema file.
- Fetches and processes data from the Congress API, including information about congress, bills, and members.
- Loads the fetched data into the database, ensuring data transformations where necessary.
- Manages database transactions, committing successful operations and rolling back in case of errors.

Note:
This file is intended to be executed directly and should not be imported as a module unless specifically required. 
Also, you require an ".env" file (README for more details) to run this file.
"""
from loguru import logger
from .sql_connection import DBConnection
from config import CONGRESS_API_KEY, CONGRESS, SETUP_SCHEMA
from logger_config import log_output, log_format, log_level
from .get_congress_data import (
    get_congress_info,
    get_bills, 
    get_members, 
    transform_members_data
)
from .db_ops import (
    initiliaze_db, 
    load_congress_data_to_db,
    load_bills_data_to_db,
    load_members_data_to_db
)


logger.remove()
logger.add(
    log_output, 
    colorize=True, 
    format=log_format,
    level=log_level
)


@logger.catch
def main(
    setup_schema: bool = False
):
    db_connection = DBConnection.get_connection()

    try:
        cursor = db_connection.cursor()
        
        if setup_schema:
            logger.info("Setting up the database schema")
            cursor.execute("BEGIN TRANSACTION;")
            initiliaze_db(db_connection, "house_votes_db_schema.sql")
            db_connection.commit()
            logger.success("Database initialized successfully")
        
        
        # Fetch congress data
        congress_df = get_congress_info(
            congress_api_key=CONGRESS_API_KEY,
            congress=CONGRESS
        )
        load_congress_data_to_db(db_connection, congress_df)
        db_connection.commit()
        logger.success("Congress data loaded successfully")
        
        # Fetch bills data
        bills_df = get_bills(
            congress_api_key=CONGRESS_API_KEY,
            congress=CONGRESS
        )
        load_bills_data_to_db(db_connection, bills_df)
        db_connection.commit()
        logger.success("Bills data loaded successfully")
        
        # Fetch members data
        members_df = get_members(
            congress_api_key=CONGRESS_API_KEY,
            congress=CONGRESS
        )
        members_df_transformed = transform_members_data(members_df)
        load_members_data_to_db(db_connection, members_df_transformed)
        db_connection.commit()
        logger.success("Members data loaded successfully")
    except Exception as e:
        db_connection.rollback()
        logger.exception(f"Error during the execution: {e}")
        return
    finally:
        db_connection.close()

    
if __name__ == "__main__":
    main(setup_schema=SETUP_SCHEMA)
