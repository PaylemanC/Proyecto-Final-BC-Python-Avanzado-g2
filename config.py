import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv(dotenv_path='.env', override=True)
    
ENVIRONMENT :str = os.getenv('ENVIRONMENT', 'PROD')
HR_VOTES_YEAR :str | None = os.getenv('HR_VOTES_YEAR', 2024)
CONGRESS_API_KEY :str = os.getenv('CONGRESS_API_KEY')
CONGRESS :str = os.getenv('CONGRESS', 118)
CONGRESS_SESSION :str = os.getenv('CONGRESS_SESSION', 2)


if __name__ == "__main__":
    print(f"ENVIRONMENT: {ENVIRONMENT}")
