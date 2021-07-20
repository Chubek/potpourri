from .scripts.get_urls import search_web
from .scripts.utils import *
from pprint import pprint
import time

class ProgrammableSearch:
    
    def __init__(self, res_num=10, step=10):
        self.results = {}
        self.step = step
        self.res_num = res_num

    def search_single_kw(self, keyword):
        start = time.time()

        urls = search_web(keyword, self.res_num, self.step)

        self.results[keyword] = {"keyword": keyword, "urls:": urls}

        end = time.time()

        print(f"Operation done in {end - start} seconds.")

        return self.results[keyword]

    def search_multiple_kw(self, keywords):
        start = time.time()

        for keyword in keywords:
            urls = search_web(keyword, self.res_num, self.step)

            self.results[keyword] = {"keyword": keyword, "urls:": urls}

        end = time.time()

        print(f"Operation done in {end - start} seconds.")

        return [self.results[keyword] for keyword in keywords]

    def search_file_kw(self, file_path, sep="\n"):
        start = time.time()

        keywords = read_and_parse_phrases(file_path, sep)

        for keyword in keywords:
            urls = search_web(keyword, self.res_num, self.step)

            self.results[keyword] =  {"keyword": keyword, "urls:": urls}

        end = time.time()

        print(f"Operation done in {end - start} seconds.")

        return [self.results[keyword] for keyword in keywords]

    def pprint_results(self):
        pprint(self.results)

    def get_results(self):
        return self.results

    def get_single_results(self, keyword):
        return self.results[get_best_match(keyword, self.results)]

    def get_multiple_results(self, keywords):
        results_to_return = []

        for kw in keywords:
            results_to_return.append(self.results[get_best_match(kw, self.results)])
        
        return results_to_return

