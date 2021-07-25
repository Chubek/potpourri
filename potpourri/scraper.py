from .scripts.scrape import *
from .scripts.keyword_extraction import *
from .scripts.request_body import get_response_body
from .scripts.store_in_dir import store_in_dir
from .scripts.get_urls import search_web
from .scripts.unqlite_interface import store_in_db
from .scripts.page_speed import get_multiple_speeds_async, get_page_speed
from .scripts.page_rank import get_page_ranks
from .scripts.utils import *
from random_word import RandomWords
from pprint import pprint
import time
import pandas as pd
import concurrent.futures

class Scraper:
    """This class encompasses all the necessary functions for scraping urls, and getting elements from them."""
    def __init__(self, min_rake_length=2, max_rake_length=4):
        """
        Instantiate a scraper.
        
        Keyword arguments:

        min_rake_length -- the minimum number of words to consider for getting keywords
        max_rake_length -- the maximum number of words to consider for getting keywords
        
        """
        self.results = {}
        self.ids_sites = {}
        self.rw = RandomWords()
        self.failures = []
        init_rake(min_rake_length, max_rake_length)


    def scrape_single(self, url, get_kw=True, custom_tags={}, custom_attrs={}, google_refer=False): 
        """
        Scrape a single url.

        Arguments:
        url -- the url to scrape
        
        Keyword arguments:
        get_kw -- get keywords
        custom_tags --- the custom tags with the attributes to get, like {"a": ["href"]}
        custom_attrs --- the custom attributes with the triggering keywords, such as {"id": ["main"]}
        google_refer --- Use Google as the referer in the request header or not
        """

        start = time.time()
        try:
            html_body = get_response_body(url, referer_google=google_refer)
        except:
            print(f"{url} timed out.")
            return None

        identifier = self.rw.get_random_word()

        while identifier in self.results or identifier is None:
            identifier = self.rw.get_random_word()
        
        try:
            self.results[identifier] = scrape(html_body, url,
            tags_to_get=custom_tags, 
            attrs_keywords_to_get=custom_attrs,
            get_keywords=get_kw)
            self.ids_sites[url] = identifier
        except:
            print(f"{url} failed to scrape.")
            return None

        end = time.time()

        print(f"Scraping operation done in {end - start} seconds.")

        return identifier

    def scrape_multiple(self, urls, get_kw=True, retry=True, custom_tags={}, custom_attrs={}, google_refer=False):
        """
        Scrape multiple urls.

        Arguments:
        url -- the url to scrape
        
        Keyword arguments:
        get_kw -- get keywords
        custom_tags --- the custom tags with the attributes to get, like {"a": ["href"]}
        custom_attrs --- the custom attributes with the triggering keywords, such as {"id": ["main"]}
        google_refer --- Use Google as the referer in the request header or not
        
        """
        
        start = time.time()
        failures = []
        identifiers = []
        for url in urls:
            print(f"Scraping url {url}")
            try:
                html_body = get_response_body(url, referer_google=google_refer)                
            except:
                print(f"{url} timed out.")
                failures.append(url)
                continue

            identifier = self.rw.get_random_word()

            while identifier in self.results or identifier is None:
                identifier = self.rw.get_random_word()

            try:
                self.results[identifier] = scrape(html_body, url,
                tags_to_get=custom_tags, 
                attrs_keywords_to_get=custom_attrs,
                get_keywords=get_kw)
                self.ids_sites[url] = identifier
                identifiers.append(identifier)
            except:
                print(f"{url} failed to scrape. If retry is enabled, it will retry at the end.")
                failures.append(url)
                continue

        end = time.time()

        print(f"Scraping operation done in {end - start} seconds.")

        if retry:
            print(f"Retry num is set to True. Now the scraper will attempt tp get the failures again...")

            for failure in failures:
                print(f"Trying to scrape {failure} again...")

                try:
                    html_body = get_response_body(failure, referer_google=google_refer)                
                except:
                    print(f"{failure} timed out. It failed again! Adding to the list of global failures.")
                    self.failures.append(failure)                
                    continue

                identifier = self.rw.get_random_word()

                while identifier in self.results or identifier is None:
                    identifier = self.rw.get_random_word()

                try:
                    self.results[identifier] = scrape(html_body, failure,
                    tags_to_get=custom_tags, 
                    attrs_keywords_to_get=custom_attrs,
                    get_keywords=get_kw)
                    self.ids_sites[failure] = identifier
                    identifiers.append(identifier)
                except:
                    print(f"{failure} failed to scrape. It failed again! Adding to the list of global failures.")
                    self.failures.append(failure)
                    continue
        else:
            print("Retry set to false. Extending global failures with local failures.")
            self.failures.extend(failures)


        return identifiers


    def scrape_multiple_parallel(self, urls, max_worker=6, get_kw=True, retry=True, custom_tags={}, custom_attrs={}, google_refer=False):
        chunks = [urls[x:x + 6] for x in range(0, len(urls), 6)]
        args = (get_kw, retry, custom_tags, custom_attrs, google_refer)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
            
            func_results = {executor.submit(self.scrape_multiple, url_chunk, *args): url_chunk for url_chunk in chunks}

            for future in concurrent.futures.as_completed(func_results):
                arg = func_results[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (arg, exc))
                else:
                    print('%r page is %d bytes' % (arg, len(data)))

    def __get_element(self, res_id, element):
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None.")
                return None

            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]
            
        return self.results[get_best_match(res_id, self.results)][element]

    def get_h1(self, res_id):
        """
        Get h1 elements.

        Arguments:
        res_id -- ID or URL.
        """ 
        return self.__get_element(res_id, "h1")

    def get_h2(self, res_id):
        """
        Get h2 elements.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "h2")

    def get_h3(self, res_id):
        """
        Get h3 elements.

        Arguments:
        res_id -- ID or URL.        
        """
        return self.__get_element(res_id, "h3")

    def get_h4(self, res_id):
        """
        Get h4 elements.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "h4")

    def get_h5(self, res_id):
        """
        Get h5 elements.

        Arguments:
        res_id -- ID or URL.
        
        """
        return self.__get_element(res_id, "h5")

    def get_h6(self, res_id):
        """
        Get h6 elements.

        Arguments:
        res_id -- ID or URL.        
        """
        return self.__get_element(res_id, "h6")

    def get_body(self, res_id):
        """
        Get body elements.

        Arguments:
        res_id -- ID or URL.        
        """
        return self.__get_element(res_id, "body")

    def get_title(self, res_id):
        """
        Get title elements.

        Arguments:
        res_id -- ID or URL.
        """
        
        return self.__get_element(res_id, "title")

    def get_html(self, res_id):
        """
        Get html elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "html")

    def get_hrefs(self, res_id):
        """
        Get href elements.

        Arguments:
        res_id -- ID or URL.        
        """
        return self.__get_element(res_id, "links")["hrefs"]

    def get_meta_desc(self, res_id):
        """
        Get meta description elements.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "meta_desc")
    
    def get_meta_keywords(self, res_id):
        """
        Get meta keywords elements.

        Arguments:
        res_id -- ID or URL.        
        """
        return self.__get_element(res_id, "meta_keywords")

    def get_meta_author(self, res_id):
        """
        Get meta author elements.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "meta_author")
    
    def get_image_alts(self, res_id):
        """
        Get image alt elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "image_alts")

    def get_bolds(self, res_id):
        """
        Get bold elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "bolds")

    def get_italics(self, res_id):
        """
        Get italic elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "italics")

    def get_lists(self, res_id):
        """
        Get list elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "lists")

    def get_strongs(self, res_id):
        """
        Get strong elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "strongs")

    def get_classics(self, res_id):
        """
        Get classic elements.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "classics")

    def get_custom_tags(self, res_id):
        """
        Get custom tags.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "custom_tags")

    def get_specific_custom_tag(self, res_id, tag):
        """
        Get get specific custom tag.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "custom_tags")[tag]

    def get_custom_attrs(self, res_id):
        """
        Get custom attributes.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "custom_attrs")

    def get_specific_custom_attr(self, res_id, attr):
        """
        Get specific cusstom attributes.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "custom_attrs")[attr]
    
    def get_internal_urls(self, res_id):
        """
        Get internal urls.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "links")["internal_urls"]

    def get_external_urls(self, res_id):
        """
        Get external urls.

        Arguments:
        res_id -- ID or URL.
        
        """
        return self.__get_element(res_id, "links")["external_urls"]

    def get_internal_urls_speeds(self, res_id):
        """
        Get page speed of internal urls urls. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "links")["internal_urls_speeds"]

    def get_external_urls_speeds(self, res_id):
        """
        Get page speed of extenral urls. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "links")["external_urls_speeds"]

    def get_internal_urls_ranks(self, res_id):
        """
        Get ranks of internal urls. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "links")["internal_urls_ranks"]

    def get_external_urls_ranks(self, res_id):
        """
        Get ranks of external urls. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "links")["external_urls_ranks"]

    def get_page_speed(self, res_id):
        """
        Get page speed. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "url")["page_speed"]

    def get_page_rank(self, res_id):
        """
        Get page rank. Must be requested first.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "url")["page_rank"]

    def get_address(self, res_id):
        """
        Get scraping url.

        Arguments:
        res_id -- ID or URL.
        """
        return self.__get_element(res_id, "url")["address"]

    def get_url_parsed(self, res_id):
        """
        Get parsed scraping url.

        Arguments:
        res_id -- ID or URL.
        """

        return self.__get_element(res_id, "url")["parsed"]

    def pprint_results(self):
        """
        Pretty print results.
        """
        pprint(self.results)

    def get_results(self):
        """
        Get results.
        """
        return self.results

    def pprint_ids(self):
        """
        Pretty print IDs.
        """
        pprint(self.ids_sites)

    def get_ids(self):       
        """
        Get IDs.
        """
        return self.ids_sites

    def get_url_id(self, url):
        """
        Get ID of single URL.

        Args:
        url -- the URL
        """
        return self.ids_sites[get_best_match(url, self.ids_sites)]

    def save_results_to_file(self, folder="~/scrape_results/jsons/"):
        """
        Save results to file.

        Args:
        folder -- the folder to save to, MUST EXIST.
        """
        for id_, res in self.results:
            store_in_dir(folder, id_, res)

    def save_results_to_db(self, db_path="~/scrape_results/scrape_results.db", db_collection="scrape_res"):
        """
        Save results to UnQlite database file.

        Keyword args:
        db_path -- path to DB
        db_collection -- name of the collection in the database.
        """

        results = list(self.results.values())

        store_in_db(db_path, db_collection, results)

    def get_single_result(self, identifier):
        """
        Get a single result.

        Args:
        identifier -- the URL or the ID.
        """
        if match_url(identifier):
            if identifier in self.failures:
                print("Url is in the list of failures, returning None.")
                return None
            identifier = self.ids_sites[get_best_match(identifier, self.ids_sites)]

        return self.results[get_best_match(identifier, self.results)]


    def get_multiple_results(self, identifiers):
        """
        Get multiple results.

        Args:
        identifiers: List of URLs or IDs. Can be mixed.
        """
        results_to_return = []

        for id_ in identifiers:
            if match_url(id_):
                if id_ in self.failures:
                    print("Url is in the list of failures, continuing...")
                    continue
                id_ = self.ids_sites[get_best_match(id_, self.ids_sites)]
            results_to_return.append(self.results[get_best_match(id_, self.results)])
        
        return results_to_return


    def request_internal_urls_speeds(self, res_id):
        """
        Request internal URL speeds.

        Args:
        res_id -- the ID or the URL
        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return None
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        internal_urls = self.get_internal_urls(res_id)

        internal_urls_speed = get_multiple_speeds_async(internal_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = internal_urls_speed

        return internal_urls_speed

   
    def request_external_urls_speeds(self, res_id):
        """
        Request external URL speeds.

        Args:
        res_id -- the ID or the URL
        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return None
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        external_urls = self.get_external_urls(res_id)

        external_urls_speed = get_multiple_speeds_async(external_urls)

        self.results[res_id]["links"]["external_urls_speeds"] = external_urls_speed

        return external_urls_speed

    def request_internal_urls_ranks(self, res_id):
        """
        Request internal URL ranks.

        Args:
        res_id -- the ID or the URL
        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return None
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        internal_urls = self.get_internal_urls(res_id)

        internal_urls_ranks = get_page_ranks(internal_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = internal_urls_ranks

        return internal_urls_ranks

    def request_external_urls_ranks(self, res_id):
        """
        Request external URL ranks.

        Args:
        res_id -- the ID or the URL
        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return None
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        external_urls = self.get_external_urls(res_id)

        external_urls_ranks = get_page_ranks(external_urls)

        self.results[res_id]["links"]["internal_urls_speeds"] = external_urls_ranks

        return external_urls_ranks

    def request_own_page_speed(self, res_id, none_val=None):
        """
        Request the scraped page speed.

        Args:
        res_id -- the ID or the URL

        Keyword args:
        none_val -- value to return if None
        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return none_val
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        url = self.results[res_id]["url"]["address"]

        page_speed = get_page_speed(url)

        self.results[res_id]["url"]["page_speed"] = page_speed

        return page_speed

    def request_own_page_speed_multiple(self, res_ids):
        """
        Request page speed for multiple IDs or urls

        Args:
        res_ids -- IDs or URLs, can be mixed
        """
        ret = {}

        for i, res_id in enumerate(res_ids):
            if match_url(res_id):
                if res_id in self.failures:
                    print("Url is in the list of failures, continuing...")
                    res_ids[i] = "didiporkhub"
                res_ids[i] = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        site_ids = dict(zip(list(self.ids_sites.values(), self.ids_sites.keys())))

        results_page_speeds = get_multiple_speeds_async([site_ids[r] for r in res_ids if r != "didiporkhub"])

        
        for res_id in res_ids:
            self.results[res_id]["url"]["page_speed"] = results_page_speeds[site_ids[res_id]]

        return results_page_speeds


    def request_own_page_rank(self, res_id, none_val=None):
        """
        Request scraped page rank.

        Args:
        res_id -- the ID or the URL

        Keyword args:
        none_val -- value to return if None

        """
        if match_url(res_id):
            if res_id in self.failures:
                print("Url is in the list of failures, returning None...")
                return none_val
            res_id = self.ids_sites[get_best_match(res_id, self.ids_sites)]

        url = self.results[res_id]["url"]["parsed"]["netloc"]

        page_rank = get_page_ranks([url])

        self.results[res_id]["url"]["page_rank"] = page_rank

        return page_rank

    def request_own_page_rank_multiple(self, res_ids):
        """
        Request page rank for multiple IDs or urls

        Args:
        res_ids -- IDs or URLs, can be mixed
        """
        ret = {}

        for res_id in res_ids:
            ret[res_id] = self.request_own_page_rank(res_id, none_val="NinaNoNo")

        return [r for r in ret if r != "NinaNoNo"]

    def reset(self):
        """
        Reset the class.
        """
        x = input("Are you sure? y/n")

        if x == "y" or x == "yes":
            self.results = {}
            self.ids_sites = {}
            print("Results were reset.")
        else:
            print("You chose no.")

    def make_pandas_df(self, keys_or_urls, descriptions=None):
        """
        Make a Pandas dataframe from the selected keywords, or urls

        Args:
        keys_or_urls: IDs or URLs, can be mixed

        Keyword args:
        descriptions: The descriptions you've got from ProgrammableSearch.

        """
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



        for i, res_id in enumerate(keys_or_urls):
            if match_url(res_id):
                if res_id in self.failures:
                    descriptions[i] = "Dupeddoodidoo"
                    print("Url is in the list of failures, continuing...")
                    continue
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
            page_speeds.append((self.get_page_speed(res_id)))
            page_ranks.append((self.get_page_rank(res_id)))

        if descriptions is None:
            descriptions = [None for _ in range(len(keys_or_urls))]
        
        df = pd.DataFrame.from_dict({"id": ids, 
                                        "url": urls,
                                        "descriptions": [d for d in descriptions if d != "Dupeddoodidoo"],
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
        


            



        
        
