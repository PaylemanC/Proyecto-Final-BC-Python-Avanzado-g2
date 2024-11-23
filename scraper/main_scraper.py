from loguru import logger
from utils import get_hr_page
from sql_connection import DBConnection
from config import CONGRESS_API_KEY, CONGRESS
from db_ops import initiliaze_db, load_members_data_to_db
from logger_config import log_output, log_format, log_level
from get_congress_data import get_members, transform_members_data


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
        
        members_df = get_members(
            congress_api_key=CONGRESS_API_KEY,
            congress=CONGRESS
        )
        members_df_transformed = transform_members_data(members_df)
        load_members_data_to_db(db_connection, members_df_transformed)
        db_connection.commit()
        logger.success("Members data loaded successfully")
        
        # hr_base_url = "https://clerk.house.gov/Votes"
        # hr_page = get_hr_page(hr_base_url)
        # logger.debug(hr_page)
    except Exception as e:
        db_connection.rollback()
        logger.exception(f"Error during the execution: {e}")
        return
    finally:
        db_connection.close()

    
if __name__ == "__main__":
    main(setup_schema=False)
