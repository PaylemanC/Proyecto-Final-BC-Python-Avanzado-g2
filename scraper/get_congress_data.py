"""
Module that contains functions to get congress data
like members, bills, etc., from the Congress API
"""
import requests
import pandas as pd
from loguru import logger
from config import CONGRESS_API_KEY, CONGRESS
from logger_config import log_format, log_output, log_level


logger.remove()
logger.add(
    log_output, 
    colorize=True, 
    format=log_format,
    level=log_level
)


@logger.catch
def get_congress_info(
    congress_api_key: str,
    congress: int
) -> pd.DataFrame:
    """
    Get the information for a given Congress number from the Congress API.
    """
    url = f"https://api.congress.gov/v3/congress/{congress}?api_key={congress_api_key}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error getting congress info: {response.status_code}")
    
    data = response.json()
    congress_info = data.get("congress", {})
    
    if not congress_info:
        raise Exception(f"No congress info found for Congress {congress}")
    
    congress_sessions = congress_info.get("sessions")
    congress_sessions_data = []
    
    for session in congress_sessions:
        session_number = session.get("number")
        session_start_date = session.get("startDate")
        session_end_date = session.get("endDate")
        
        session_data = {
            "congress_id": f"{congress}-{session_number}",
            "session": session_number,
            "number": congress,
            "start_date": session_start_date,
            "end_date": session_end_date
        }
        congress_sessions_data.append(session_data)
    logger.debug(f"Congress sessions data: {congress_sessions_data}")
        
    congress_df = pd.DataFrame(congress_sessions_data).drop_duplicates()
    return congress_df


@logger.catch
def get_bills(
    congress_api_key: str,
    congress: int
) -> pd.DataFrame:
    """
    Fetch bills for a given Congress number 
    from the Congress API.

    Each bill includes:
    - bill_id
    - number
    - type
    - description (from 'title')
    
    Params:
        congress_api_key (str): The API key for the Congress API
        congress (int): The Congress number
    
    Returns:
        pd.DataFrame: A DataFrame containing the bills data.
    """
    url = f"https://api.congress.gov/v3/bill/{congress}?api_key={congress_api_key}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error getting bills: {response.status_code}")
    
    data = response.json()
    bills_response: list = data.get("bills", [])
    
    bills_data: list = []
    
    for bill in bills_response:
        try:
            bill_number = bill.get("number")
            bill_type = bill.get("type")
            bill_description = bill.get("title")
            latest_action = bill.get("latestAction", {})
            action_date = latest_action.get("actionDate", None) 
            action_text = latest_action.get("text", None) 
            
            bill_data = {
                "bill_id": f"{bill_number}-{bill_type}",  
                "number": bill_number,
                "type": bill_type,
                "description": bill_description,
                "action_date": action_date, 
                "action_text": action_text
            }
            bills_data.append(bill_data)
        except KeyError as ke:
            logger.error(f"Key: {ke} not found in bill: {bill.get('number')}")
            continue

    if not bills_data:
        logger.warning(f"No bills found for Congress {congress}")
    else:
        logger.info(f"Retrieved {len(bills_data)} bills for Congress {congress}")

    #TODO: Add pagination to extract all bills for a congress
    
    bills_df = pd.DataFrame(bills_data)
    logger.success(f"Bills data processed successfully")
    return bills_df


@logger.catch
def get_members(
    congress_api_key: str,
    congress: int, 
    offset: int = 0,
    limit: int = 50
) -> pd.DataFrame:
    """
    Get the members of the Congress
    for a given congress from the Congress API.
    
    For each member, the following data is fetched:
    - member_id
    - name
    - image_url
    - party
    - state
    
    Params:
        congress_api_key (str): The API key for the Congress API
        congress (int): The Congress number
        offset (int): The offset for the API request
        limit (int): The limit for the API request
    """
    url = f"https://api.congress.gov/v3/member/congress/{congress}?api_key={congress_api_key}&format=json&offset={offset}&limit={limit}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f'Error getting members: {response.status_code}')
    
    data = response.json()
    response_count = data['pagination']['count']
    logger.debug(f'Response count: {response_count}')
    
    members_response :list = data['members']
    members_final_data :list = []
    
    
    def get_member_data(members_response: list[dict]) -> list[dict]:
        for member in members_response:
            try:
                member_data = {
                    'member_id': member['bioguideId'],
                    'name': member['name'],
                    'party': member['partyName'],
                    'state': member['state']
                }
                
                default_image_url = "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg"
                
                member_data['image_url'] = member.get('depiction', {}).get('imageUrl', default_image_url)
            except KeyError as ke:
                logger.error(f"Key: {ke} not found for member: {member['bioguideId']}")
                continue
            
            members_final_data.append(member_data)
    
    get_member_data(members_response)
    logger.info(f"Processed {len(members_final_data)} of {response_count} members")
    
    while True:
        offset += limit
        url = data['pagination'].get('next', None)
        
        if url is None:
            break
        
        url += f"&api_key={congress_api_key}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Error getting members at offset {offset}. Status code: {response.status_code} ")
        
        data = response.json()
        members_response :list = data['members']
        get_member_data(members_response)
                
        
        logger.info(f"Processed {len(members_final_data)} of {response_count} members")
    
    members_df = pd.DataFrame(members_final_data)
    logger.success(f"All congress members processed successfully")
    return members_df


@logger.catch
def transform_members_data(
    members_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Transform the members data to match the 'members' table schema
    by mapping the party and state to their respective codes
    """
    states_codes = {
        'Alabama': 'AL',
        'Alaska': 'AK', 
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virgin Islands': 'VI',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }
    
    parties_codes = {
        'Democratic': 'D',
        'Republican': 'R',
        'Independent': 'I'
    }
    
    members_df['state'] = members_df['state'].map(states_codes)
    members_df['party'] = members_df['party'].map(parties_codes)
    
    return members_df


if __name__ == '__main__':    
    congress_info :pd.DataFrame = get_congress_info(
        congress_api_key=CONGRESS_API_KEY,
        congress=CONGRESS
    )