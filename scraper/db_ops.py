'''
This module provides utility functions to manage database operations for the project. 

Responsibilities:
- Initialize the database schema using an SQL script.
- Load data into the database from pandas DataFrames, including handling conflicts and updates.
- Functions are designed to work with a database connection and execute bulk operations efficiently.
'''
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
    
    Args:
        db_connection: The database connection object.
        congress_df (DataFrame): A pandas DataFrame containing Congress session data with the following columns:
            - congress_id
            - session
            - number
            - start_date
            - end_date
    """
    values = [tuple(row) for row in congress_df.values]
    logger.info(f"Loading {len(values)} records to the 'congress' table")
    insert_query = """
        INSERT INTO congress (congress_id, session, number, start_date, end_date) 
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(congress_id) DO UPDATE SET
            session = excluded.session,
            number = excluded.number,
            start_date = excluded.start_date,
            end_date = excluded.end_date
    """
    db_connection.executemany(insert_query, values)
    

def load_members_data_to_db(
    db_connection,
    members_df
):
    """
    Load the members data to the database.
    
    Args:
        db_connection: The database connection object.
        members_df (DataFrame): A pandas DataFrame containing Congress member data with the following columns:
            - member_id
            - name
            - image_url
            - party
            - state
    """
    values = [
        (
            row["member_id"],
            row["name"],
            row["image_url"],
            row["party"],
            row["state"]
        )
        for _, row in members_df.iterrows()
    ]
    
    logger.info(f"Loading {len(values)} members to the database")
    insert_query = """
        INSERT INTO members (member_id, name, image_url, party_code, state_code) 
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(member_id) DO UPDATE SET
            name = excluded.name,
            image_url = excluded.image_url,
            party_code = excluded.party_code,
            state_code = excluded.state_code
    """
    db_connection.executemany(insert_query, values)


def load_bills_data_to_db(
    db_connection,
    bills_df
):
    """
    Load the bills data to the database.
    
    Args:
        db_connection: The database connection object.
        bills_df (DataFrame): A pandas DataFrame containing bill data with the following columns:
            - bill_id
            - number
            - type
            - description
            - action_date
    """
    values = [
        (
            row["bill_id"],          
            row["number"],       
            row["type"],         
            row["description"],        
            row["action_date"], 
            row["action_text"],
        )
        for _, row in bills_df.iterrows()
    ]

    logger.info(f"Loading {len(values)} bills to the database")

    insert_query = """
        INSERT INTO bills (bill_id, number, type, description, action_date, action_text) 
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(bill_id) DO UPDATE SET
            number = excluded.number,
            type = excluded.type,
            description = excluded.description,
            action_date = excluded.action_date,  
            action_text = excluded.action_text
    """
    db_connection.executemany(insert_query, values)
