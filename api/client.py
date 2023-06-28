import json
import requests
from api_settings import API_ENDPOINT_URL, get_credentials, APP_VERSION

OK_RESPONSE_CODES = [200, 201] 

class Client:

    def __init__(self, token=None, version=APP_VERSION):
        self.client = requests.Session()
        token = token if token else get_credentials()
        headers = {
            "Authorization": f"Token {token}",
            "Accept": f"application/json;version={version}"
            }
        self.client.headers.update(headers)
    
    def send_query(self, query, return_raw=False):
        r = self.client.get(query)
        if return_raw:
                return r
        if r.status_code in OK_RESPONSE_CODES:
            
            return r.json()
        else:
            error = {"status": r.status_code, "message": r.reason}
            return error
    
    def post_query(self, query, post_data):
        r = self.client.post(query, data=post_data)
        if r.status_code in OK_RESPONSE_CODES:
            return r.json()
        else:
            error = {"status": r.status_code, "message": r.reason}
            return error, r.json()
