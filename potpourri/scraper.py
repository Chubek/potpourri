from .scripts.scrape import *
from .scripts.keyword_extraction import *
from .scripts.request_body import get_response_body
from .scripts.store_in_dir import store_in_dir
from .scripts.get_urls import search_web
from .scripts.unqlite_interface import store_in_db
from .scripts.page_speed import get_page_speed_multiple
from .scripts.page_rank import get_page_ranks

from random_word import RandomWords
from pprint import pprint
from .scripts.utils import *
import time

class Scraper:
    def __init__(self, min_rake_length=2, max_rake_length=4):
        self.results = {}
        self.ids_sites = {}
        self.rw = RandomWords()
        init_rake(min_rake_length, max_rake_length)


    def scrape_single(self, url, get_kw=True, custom_tags={}, custom_attrs={}, google_refer=False):   
        start = time.time()
        html_body = get_response_body(url, referer_google=google_refer)
        
        identifier = self.rw.get_random_word()

        while identifier in self.results or identifier is None:
            identifier = self.rw.get_random_word()
                
        self.results[identifier] = scrape(html_body, url,
         tags_to_get=custom_tags, 
         attrs_keywords_to_get=custom_attrs,
         get_keywords=get_kw)
        self.ids_sites[url] = identifier
        
        end = time.time()

        print(f"Operation done in {end - start} seconds.")

        return identifier

    def scrape_multiple(self, urls, get_kw=True, custom_tags={}, custom_attrs={}, google_refer=False):
        start = time.time()

        identifiers = {}
        for url in urls:
            html_body = get_response_body(url, referer_google=google_refer)
            identifier = self.rw.get_random_word()

            while identifier in self.results or identifier is None:
                identifier = self.rw.get_random_word()

            self.results[identifier] = scrape(html_body, url,
                tags_to_get=custom_tags, 
                attrs_keywords_to_get=custom_attrs,
                get_keywords=get_kw)
            self.ids_sites[url] = identifier
            identifiers[url] = identifier
        end = time.time()

        print(f"Operation done in {end - start} seconds.")

        return identifiers


    def __get_element(self, res_id, element):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]
            
        return self.results[get_best_match(res_id, self.results)][element]

    def get_h1(self, res_id): 
        return self.__get_element(res_id, "h1")

    def get_h2(self, res_id):
        return self.__get_element(res_id, "h2")

    def get_h3(self, res_id):
        return self.__get_element(res_id, "h3")

    def get_h4(self, res_id):
        return self.__get_element(res_id, "h4")

    def get_h5(self, res_id):
        return self.__get_element(res_id, "h5")

    def get_h6(self, res_id):
        return self.__get_element(res_id, "h6")

    def get_body(self, res_id):
        return self.__get_element(res_id, "body")

    def get_title(self, res_id):
        return self.__get_element(res_id, "title")

    def get_html(self, res_id):
        return self.__get_element(res_id, "html")

    def get_hrefs(self, res_id):
        return self.__get_element(res_id, "links")["hrefs"]

    def get_meta_desc(self, res_id):
        return self.__get_element(res_id, "meta_desc")
    
    def get_meta_keywords(self, res_id):
        return self.__get_element(res_id, "meta_keywords")

    def get_meta_author(self, res_id):
        return self.__get_element(res_id, "meta_author")
    
    def get_image_alts(self, res_id):
        return self.__get_element(res_id, "image_alts")

    def get_bolds(self, res_id):
        return self.__get_element(res_id, "bolds")

    def get_italics(self, res_id):
        return self.__get_element(res_id, "italics")

    def get_lists(self, res_id):
        return self.__get_element(res_id, "lists")

    def get_strongs(self, res_id):
        return self.__get_element(res_id, "strongs")

    def get_classics(self, res_id):
        return self.__get_element(res_id, "classics")

    def get_custom_tags(self, res_id):
        return self.__get_element(res_id, "custom_tags")

    def get_specific_custom_tag(self, res_id, tag):
        return self.__get_element(res_id, "custom_tags")[tag]

    def get_custom_attrs(self, res_id):
        return self.__get_element(res_id, "custom_attrs")

    def get_specific_custom_attr(self, res_id, attr):
        return self.__get_element(res_id, "custom_attrs")[attr]
    
    def get_internal_urls(self, res_id):
        return self.__get_element(res_id, "links")["internal_urls"]

    def get_external_urls(self, res_id):
        return self.__get_element(res_id, "links")["external_urls"]

    def get_internal_urls_speeds(self, res_id):
        return self.__get_element(res_id, "links")["internal_urls_speeds"]

    def get_external_urls_speeds(self, res_id):
        return self.__get_element(res_id, "links")["external_urls_speeds"]

    def get_internal_urls_ranks(self, res_id):
        return self.__get_element(res_id, "links")["internal_urls_ranks"]

    def get_external_urls_ranks(self, res_id):
        return self.__get_element(res_id, "links")["external_urls_ranks"]

    def get_page_speed(self, res_id):
        return self.__get_element(res_id, "url")["page_speed"]

    def get_page_rank(self, res_id):
        return self.__get_element(res_id, "url")["page_rank"]

    def pprint_results(self):
        pprint(self.results)

    def get_results(self):
        return self.results

    def pprint_ids(self):
        pprint(self.ids_sites)

    def get_ids(self):
        return self.ids_sites

    def get_url_id(self, url):
        return self.ids_sites[get_best_match(url, self.ids_sites)]

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


    def request_internal_urls_speeds(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        internal_urls = self.get_internal_urls(res_id)

        internal_urls_speed = get_page_speed_multiple(internal_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = internal_urls_speed

        return internal_urls_speed

   
    def request_external_urls_speeds(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        external_urls = self.get_external_urls(res_id)

        external_urls_speed = get_page_speed_multiple(external_urls)

        self.results[res_id]["links"]["external_urls_speeds"] = external_urls_speed

        return external_urls_speed

    def request_internal_urls_ranks(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        internal_urls = self.get_internal_urls(res_id)

        internal_urls_ranks = get_page_ranks(internal_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = internal_urls_ranks

        return internal_urls_ranks

    def request_external_urls_ranks(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        external_urls = self.get_external_urls(res_id)

        external_urls_ranks = get_page_ranks(external_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = external_urls_ranks

        return external_urls_ranks

        

        
        
