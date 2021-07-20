import nltk
from rake_nltk import Rake

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

r = None

def init_rake(min_word, max_word):
    global r, parse_patterns
    r = Rake(min_length=min_word, max_length=max_word)


def kword(txt):
    r.extract_keywords_from_text(txt)

    return r.get_ranked_phrases()
