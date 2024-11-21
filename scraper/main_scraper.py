from loguru import logger
from utils import get_hr_page
from db_ops import initiliaze_db
from sql_connection import DBConnection
from logger_config import log_output, log_format, log_level


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
            cursor.execute("BEGIN TRANSACTION;")
            initiliaze_db(db_connection, "house_votes_db_schema.sql")
            db_connection.commit()
            logger.success("Database initialized successfully")
        
        # hr_base_url = "https://clerk.house.gov/Votes"
        # hr_page = get_hr_page(hr_base_url)
        # logger.debug(hr_page)
    except Exception as e:
        db_connection.rollback()
        logger.exception(f"Error initializing the database: {e}")
        return
    finally:
        db_connection.close()

    
if __name__ == "__main__":
    main(setup_schema=True)
