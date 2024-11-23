'''
Module that contains functions to get congress data
like members, bills, etc., from the Congress API
'''
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
def get_members(
    congress_api_key: str,
    congress: int, 
    offset: int = 0,
    limit: int = 50
) -> pd.DataFrame:
    """
    Get the members of the Congress
    for a given congress.
    
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
                    'image_url': member['depiction']['imageUrl'],
                    'party': member['partyName'],
                    'state': member['state']
                }
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


if __name__ == '__main__':
    members :pd.DataFrame = get_members(
        congress_api_key=CONGRESS_API_KEY, 
        congress=CONGRESS
    )
    members.to_csv('members.csv', index=False)
