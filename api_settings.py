from os import getenv
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = getenv('ENVIRONMENT', 'staging')

APP_VERSION = "1.2.0"

API_ENDPOINT_URL = {
    "local": getenv('LOCAL_URL'),
    "staging": getenv('STAGING_URL')
}

credentials = {
    "local": getenv('LOCAL_API_KEY'),
    "staging": getenv('STAGING_API_KEY')
}

def get_credentials():
    """Returns token for the environment test user"""
    return credentials.get(ENVIRONMENT)

def get_endpoint():
    """Returns the API endpoint 'https://.../api/'"""
    return API_ENDPOINT_URL.get(ENVIRONMENT)