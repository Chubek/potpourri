from potpourri.scripts.scrape import scrape
import unittest
from potpourri.scraper import Scraper
from pprint import pprint

class TesScraper(unittest.TestCase):
    def test_scraper_simple(self):
        scraper = Scraper()

        res = scraper.scrape_single("https://en.wikipedia.org/wiki/1945")

        pprint(res)

        self.assertEqual(res['title']['whole'], "1945 - Wikipedia")