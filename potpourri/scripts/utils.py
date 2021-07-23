from difflib import SequenceMatcher
import re
import threading
from urllib.parse import urlparse

url_regex = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

def match_url(txt):
    return re.match(url_regex, txt) is not None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def read_and_parse_phrases(path, sep):
    with open(path, "r") as f:
        whole_text = f.read()

    phrases = [re.sub(r"\s+", " ", p.strip()) for p in whole_text.split(sep)]

    return phrases

def get_best_match(given_key, given_dict):
    if given_key in given_dict:
        return given_key


    matches = {}
    ids = list(given_dict.keys())

    for id_ in ids:
        matches[id_] = similar(given_key, id_)

    sorted_dict = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}

    best_possibility = list(sorted_dict.keys())[-1]

    if list(sorted_dict.values())[-1] <= 0.5:
        print(f"Key/Url {given_key} did not exist in the list but was matched with {best_possibility}. However, given their similarity({list(sorted_dict.values())[-1]}), it seems like your key/url does not exist in the list at all. It probably timed out or failed to scrape. Be wary.")
        return best_possibility

    print(f"Key/Url {given_key} did not exist in the list but was matched with {best_possibility}.")
    return best_possibility

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def find_all_words(txt):
    return len(re.findall(r"(\w+)", txt))


def filter_list(list):
    return [re.sub(r"\s+", " ", l.strip()) for l in list if len(l) > 1 and not re.match(r"[^A-Za-z0-9]", l)]

def flatten_list(lists):
    return sum(lists, [])

def check_internal(main_url, url):
    if not "http" in main_url:
        main_url = "http://" + main_url

    if not "http" in url:
        url = "http://" + url

    main_parse = urlparse(main_url)
    url_parse = urlparse(url)

    return main_parse.netloc == url_parse.netloc


def split_internal_external(main_url, hrefs):
    internal_urls = [url for url in hrefs if check_internal(main_url, url)]
    external_urls = [url for url in hrefs if not check_internal(main_url, url)]


    return internal_urls, external_urls

def parse_url(url):
    if not "http" in url:
        url = "http://" + url

    url_parsed = urlparse(url)

    return {"netloc": url_parsed.netloc, 
        "scheme": url_parsed.scheme, 
        "path": url_parsed.path, 
        "params": url_parsed.params, 
        "query": url_parsed.query, 
        "fragment": url_parsed.fragment}