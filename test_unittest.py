import unittest
from utils import extract_data, match, find_link
import requests
        
class TestScrapeGoogle(unittest.TestCase):

    def test_scrape_google(self):
        self.assertEqual(find_link("whatsapp"), "https://whatsapp.en.aptoide.com/app", "Should be whatsapp link")

    def test_scrape_google_2(self):
        self.assertNotEqual(find_link("facebook"), "https://whatsapp.en.aptoide.com/app", "Should not be whatsapp link")
        
class TestMatch(unittest.TestCase):

    def test_match(self):
        self.assertTrue(match("https://facebook.en.aptoide.com/app"), "Should match")

    def test_match_2(self):
        self.assertFalse(match("https://facebook.com/app"), "Should not match")

class TestExtractData(unittest.TestCase):

    def test_extract_data(self):
        self.assertEqual(list(extract_data(requests.get("https://facebook.en.aptoide.com/app"))), ["Name","Version","Downloads","Description","Release Date"], "Should return corresponding fields")
        
    def test_extract_data_2(self):
        self.assertEqual(extract_data(requests.get("https://youtube.com/app")), None,"Should return None")
    

        
if __name__ == '__main__':
    unittest.main()
