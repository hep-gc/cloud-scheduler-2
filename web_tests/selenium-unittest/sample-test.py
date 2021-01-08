import unittest
from selenium import webdriver

class SampleTest(unittest.TestCase):
    """A class to do a few small, simple tests as a trial run for selenium and
       unittest."""

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_first(self):
        self.assertTrue(True)

    def test_find_element(self):
        self.driver.get("https://google.com")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
