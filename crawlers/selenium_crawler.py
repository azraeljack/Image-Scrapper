from .base_crawler import BaseCrawler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver


class SeleniumCrawler(BaseCrawler):

    def __init__(self, **kwargs):
        self.browser = webdriver.PhantomJS('../resource/phantomjs/phantomjs')
        super(SeleniumCrawler, self).__init__(**kwargs)

    def crawl(self, url):
        self.browser.get(url)
        WebDriverWait(self.browser, 10).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
        )

        return self.browser.page_source
