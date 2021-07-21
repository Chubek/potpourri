import requests
import os

def get_page_ranks(urls):
    headers = {
        "API-OPR": os.environ["OPR_API_KEY"]
    }

    req = requests.get(f"https://openpagerank.com/api/v1.0/getPageRank?domains[]=[{','.join(urls)}]", 
            headers=headers)

    if req.status_code != 200:
        return {}

    return req.json()
