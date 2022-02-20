import requests


def get_response_body(url, referer_google=True):
    
    headers = {
        "accept": "*/* ",
        "accept-encoding": "deflate",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.google.com/",
        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
        "sec-ch-ua-mobile": "?0",
        "ec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    if not referer_google:
        headers.pop("referer", None)
    
    req = requests.get(url, headers=headers)

    return req.content


