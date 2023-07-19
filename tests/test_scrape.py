import unittest
from src.utils import FakeUserAgent, header_dictionary
from scraper_exceptions.exceptions import NumError,UACreateError,ZeroResultsError
from src.gse import GoogleSearchUrls, GoogleSearchSimilarity

class TestScraper(unittest.TestCase):
    def test_ua(self):
        self.assertEqual(type(FakeUserAgent().fake_ua()),str,"Incorrect user-agent.")
    def test_header(self):
        self.assertEqual(type(header_dictionary()),dict,"Incorrect headers.")
    def test_gse_simi(self):
        self.assertEqual(type(GoogleSearchSimilarity().score(search_string="Writing unit and integration tests in python.",num_results=10,wait_time=10)),dict,"Invalid similarity score format.")

unittest.main()