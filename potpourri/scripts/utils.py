from difflib import SequenceMatcher
import re
import threading
import functools
import operator

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

def flatten_list(list):
    return functools.reduce(operator.iconcat, list, [])