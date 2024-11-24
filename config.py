import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv(dotenv_path='.env', override=True)
    
ENVIRONMENT :str = os.getenv('ENVIRONMENT', 'PROD')
SETUP_SCHEMA :bool = os.getenv('SETUP_SCHEMA', False)
CONGRESS :str = os.getenv('CONGRESS', 118)
CONGRESS_API_KEY :str = os.getenv('CONGRESS_API_KEY')


if __name__ == "__main__":
    print(f"ENVIRONMENT: {ENVIRONMENT}")
