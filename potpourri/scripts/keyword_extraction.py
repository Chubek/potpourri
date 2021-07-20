import re
import nltk
nltk.download('stopwords')
from rake_nltk import Rake

r = None

def init_rake(min_word, max_word):
    global r, parse_patterns
    r = Rake(min_length=min_word, max_length=max_word)


def kword(txt):
    r.extract_keywords_from_text(txt)

    return r.get_ranked_phrases()
