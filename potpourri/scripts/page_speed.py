import requests
import os

def get_page_speed(url):
    req = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={os.environ["GOOGLE_API_KEY"]}')

    if req.status_code != 200:
        return {}

    return req.json()


def get_page_speed_multiple(urls):
    res = {}

    for url in urls:
        res[url] = get_page_speed(url)

    return res