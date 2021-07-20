from .scripts.scrape import *
from .scripts.keyword_extraction import *
from .scripts.request_body import get_response_body
from .scripts.store_in_dir import store_in_dir
from .scripts.get_urls import search_web
from .scripts.unqlite_interface import store_in_db
from random_word import RandomWords
from pprint import pprint
from .scripts.utils import *


class Scraper:
    def __init__(self, min_rake_length=2, max_rake_length=4):
        self.results = {}
        self.ids_sites = {}
        self.rw = RandomWords()
        init_rake(min_rake_length, max_rake_length)


    def scrape_single(self, url, get_kw=True, custom_tags={}, custom_attrs={}, google_refer=False):   

        html_body = get_response_body(url, referer_google=google_refer)
        
        identifier = self.rw.get_random_word()
                
        self.results[identifier] = scrape(html_body, url,
         tags_to_get=custom_tags, 
         attrs_keywords_to_get=custom_attrs,
         get_keywords=get_kw)
        self.ids_sites[url] = identifier

        return identifier

    def scrape_multiple(self, urls, get_kw=True, custom_tags={}, custom_attrs={}, google_refer=False):
        identifiers = {}
        for url in urls:
            html_body = get_response_body(url, referer_google=google_refer)
            identifier = self.rw.get_random_word()
            self.results[identifier] = scrape(html_body, url,
                tags_to_get=custom_tags, 
                attrs_keywords_to_get=custom_attrs,
                get_keywords=get_kw)
            self.ids_sites[url] = identifier
            identifiers[url] = identifier

        return identifiers

    def get_h1(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['h1']

    def get_h2(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['h2']

    def get_h3(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['h3']

    def get_h4(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['h4']

    def get_h5(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['h5']

    def get_h6(self, res_id):
        return self.results[res_id]['h6']

    def get_body(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['body']

    def get_title(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['title']
    
    def get_html(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['html']

    def get_hrefs(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['hrefs']

    def get_meta_desc(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['meta_desc']
    
    def get_meta_keywords(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['meta_keywords']

    def get_meta_author(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['meta_author']
    
    def get_image_alts(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['image_alts']

    def get_bolds(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['bolds']

    def get_italics(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['italics']

    def get_lists(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['lists']

    def get_strongs(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['strongs']

    def get_classics(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['classics']

    def get_custom_tags(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['custom_tags']

    def get_custom_attrs(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]

        return self.results[res_id]['custom_attrs']

    def get_lengths(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[res_id]
            
        return self.results[res_id]['lengths']

    def pprint_results(self):
        pprint(self.results)

    def get_results(self):
        return self.results

    def pprint_ids(self):
        pprint(self.ids_sites)

    def get_ids(self):
        return self.ids_sites

    def save_results_to_file(self, folder="~/scrape_results/jsons/"):
        for id_, res in self.results:
            store_in_dir(folder, id_, res)

    def save_results_to_db(self, db_path="~/scrape_results/scrape_results.db", db_collection="scrape_res"):
        results = list(self.results.values())

        store_in_db(db_path, db_collection, results)

    def get_single_result(self, identifier):
        if match_url(identifier):
            identifier = self.ids_sites[get_best_match(identifier, self.ids_sites)]

        return self.results[get_best_match(identifier, self.results)]


    def get_multiple_results(self, identifiers):
        results_to_return = []

        for id_ in identifiers:
            if match_url(id_):
                id_ = self.ids_sites[get_best_match(id_, self.ids_sites)]
            results_to_return.append(self.results[get_best_match(id_, self.results)])
        
        return results_to_return

class ProgrammableSearch:
    
    def __init__(self, res_num=10, step=10):
        self.results = {}
        self.step = step
        self.res_num = res_num

    def search_single_kw(self, keyword):
        urls = search_web(keyword, self.res_num, self.step)

        self.results[keyword] = {"keyword": keyword, "urls:": urls}

        return self.results[keyword]

    def search_multiple_kw(self, keywords):
        for keyword in keywords:
            urls = search_web(keyword, self.res_num, self.step)

            self.results[keyword] = {"keyword": keyword, "urls:": urls}

        return [self.results[keyword] for keyword in keywords]

    def search_file_kw(self, file_path, sep="\n"):
        keywords = read_and_parse_phrases(file_path, sep)

        for keyword in keywords:
            urls = search_web(keyword, self.res_num, self.step)

            self.results[keyword] =  {"keyword": keyword, "urls:": urls}

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



class ConcurrentRun:
    def __init__(self):
        self.results = {}
        
        
    def run_concurrent_noargs_single(self, func, parallel=True, number_of_threads=5):
        threads = {}
        results = {}

        for i in range(number_of_threads):
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(target=func, args=())

        for func_name, thread in threads.items():
            thread.start()

            if not parallel:
                thread.join()
                results[func_name] = thread.result

        if parallel:
            for func_name, thread in threads.items():
                thread.join()
                results[func_name] = thread.result

        return results

    def run_concurrent_noargs_multiple(self, funcs, parallel=True, number_of_threads=5):        
        results = {}

        for func in funcs:
            results[func.__name__] = self.run_concurrent_noargs_single(func, 
            parallel=parallel, 
            number_of_threads=number_of_threads)

        return results
        

    def run_concurrent_args_single(self, func, args, parallel=True, number_of_threads=5):
        threads = {}
        results = {}

        for i in range(number_of_threads):
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(target=func, args=(*args, ))

        for func_name, thread in threads.items():
            thread.start()

            if not parallel:
                thread.join()
                results[func_name] = thread.result

        if parallel:
            for func_name, thread in threads.items():
                thread.join()
                results[func_name] = thread.result

        return results

    def run_concurrent_args_multiple(self, funcs, args, parallel=True, number_of_threads=5):        
        results = {}

        for func in funcs:
            results[func.__name__] = self.run_concurrent_noargs_single(func, args,
            parallel=parallel, 
            number_of_threads=number_of_threads)

        return results


