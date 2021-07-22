from .scripts.scrape import *
from .scripts.keyword_extraction import *
from .scripts.request_body import get_response_body
from .scripts.store_in_dir import store_in_dir
from .scripts.get_urls import search_web
from .scripts.unqlite_interface import store_in_db
from .scripts.page_speed import get_page_speed_multiple, get_page_speed
from .scripts.page_rank import get_page_ranks
from .scripts.utils import *
from random_word import RandomWords
from pprint import pprint
import time
import pandas as pd

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

        identifiers = []
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
            identifiers.append(identifier)
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

    def get_address(self, res_id):
        return self.__get_element(res_id, "url")["address"]

    def get_url_parsed(self, res_id):
        return self.__get_element(res_id, "url")["parsed"]

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

    def request_own_page_speed(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        url = self.results[res_id]["url"]["address"]

        page_speed = get_page_speed(url)

        self.results[res_id]["url"]["page_speed"] = page_speed

        return page_speed

    def request_own_page_speed_multiple(self, res_ids):
        ret = {}

        for res_id in res_ids:
            ret[res_id] = self.request_own_page_speed(res_id)

        return ret

    def request_own_page_rank(self, res_id):
        if match_url(res_id):
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        url = self.results[res_id]["url"]["parsed"]["netloc"]

        page_rank = get_page_ranks([url])

        self.results[res_id]["url"]["page_rank"] = page_rank

        return page_rank

    def request_own_page_rank_multiple(self, res_ids):
        ret = {}

        for res_id in res_ids:
            ret[res_id] = self.request_own_page_rank(res_id)

        return ret

    def make_pandas_df(self, keys_or_urls):
        urls = []
        ids = []
        htmls = []
        bodies = []
        h1s = []
        h2s = []
        h3s = []
        h4s = []
        h5s = []
        h6s = []
        hrefs = []
        internal_links = []
        external_links = []
        meta_descs = []
        meta_authors = []
        titles = []
        classics = []
        meta_keywords = []
        image_alts = []
        bolds = []
        italics = []
        lists = []
        strongs = []
        custom_tags = []
        custom_attrs = []
        parsed_urls = []
        page_speeds = []
        page_ranks = []

        for res_id in keys_or_urls:
            if match_url(res_id):
                res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

            urls.append(self.get_address(res_id))
            ids.append(res_id)
            htmls.append(self.get_html(res_id))
            titles.append(self.get_title(res_id))
            bodies.append(self.get_body(res_id))
            h1s.append(self.get_h1(res_id))
            h2s.append(self.get_h2(res_id))
            h3s.append(self.get_h3(res_id))
            h4s.append(self.get_h4(res_id))
            h5s.append(self.get_h5(res_id))
            h6s.append(self.get_h6(res_id))
            hrefs.append(self.get_hrefs(res_id))
            internal_links.append(self.get_internal_urls(res_id))
            external_links.append(self.get_external_urls(res_id))
            meta_descs.append(self.get_meta_desc(res_id))
            meta_authors.append(self.get_meta_author(res_id))
            meta_keywords.append(self.get_meta_keywords(res_id))
            image_alts.append(self.get_image_alts(res_id))
            bolds.append(self.get_bolds(res_id))
            italics.append(self.get_italics(res_id))
            strongs.append(self.get_strongs(res_id))
            custom_tags.append(self.get_custom_tags(res_id))
            custom_attrs.append(self.get_custom_attrs(res_id))
            lists.append(self.get_lists(res_id))
            classics.append(self.get_classics(res_id))
            parsed_urls.append(self.get_url_parsed(res_id))
            page_speeds.append(self.get_page_speed(res_id))
            page_ranks.append(self.get_page_ranks(res_id))

        df = pd.DataFrame.from_dict({"id": ids, 
                                        "url": urls,
                                        "parsed_url": parsed_urls,
                                        "page_speed": page_speeds,
                                        "page_rank": page_ranks,                                        
                                        "html": htmls,
                                        "title": titles,
                                        "body": bodies,
                                        "classic": classics,
                                        "h1": h1s,
                                        "h2": h2s,
                                        "h3": h3s,
                                        "h4": h4s,
                                        "h5": h5s,
                                        "h6": h6s,
                                        "href": hrefs,
                                        "internal_links": internal_links,
                                        "external_links": external_links,
                                        "meta_desc": meta_descs,
                                        "meta_keywords": meta_keywords,
                                        "meta_author": meta_authors,
                                        "image_alts": image_alts,
                                        "bolds": bolds,
                                        "italics": italics,
                                        "strongs": strongs,
                                        "lists": lists,
                                        "custom_tags": custom_tags,
                                        "custom_attrs": custom_attrs})

        return df
        
            



        
        
