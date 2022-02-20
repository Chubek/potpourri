import requests
import os

def get_page_ranks(urls):
    headers = {
        "API-OPR": os.environ["OPR_API_KEY"]
    }

    query = f"domains[]={urls[0]}"

    for url in urls[1:]:
        query += f"&domains[]={url}"

    req = requests.get(f"https://openpagerank.com/api/v1.0/getPageRank?{query}", 
            headers=headers)

    if req.status_code != 200:
        return {}

    return req.json()
