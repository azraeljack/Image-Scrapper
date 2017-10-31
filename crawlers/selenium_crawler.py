from .base_crawler import BaseCrawler
from exceptions import InvalidParamException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep


class SeleniumCrawler(BaseCrawler):
    DEFAULT_CONFIG = {
        'page_timeout': 10,
        'web_driver': 'phantomjs',
        'executable_path': '../resource/phantomjs/phantomjs',
        'scroll_to_bottom': False,
        'scroll_pause_time': 0.5,
        'max_scroll_times': 65535  # Add this to avoid to many scrolls
    }

    WEB_DRIVERS = {
        'phantomjs': webdriver.PhantomJS,
        'chrome': webdriver.Chrome,
        'firefox': webdriver.Firefox,
        'edge': webdriver.Edge,
        'safari': webdriver.Safari
    }

    def __init__(self, **config):
        self.config = self._parse_config(config)
        driver_class = self.WEB_DRIVERS[self.config.get('web_driver', 'phantomjs').lower()]

        executable_path = self.config.get('executable_path')

        if not executable_path:
            raise InvalidParamException('Invalid executable path provided.')

        self.browser = driver_class(executable_path)
        super(SeleniumCrawler, self).__init__(**config)

    def _get_current_height(self):
        return self.browser.execute_script('return document.body.scrollHeight;')

    def crawl(self, url):
        self.browser.get(url)
        WebDriverWait(self.browser, self.config['page_timeout']).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'body'))
        )

        if self.config['scroll_to_bottom']:
            self.scroll_to_bottom()

        return self.browser.page_source

    def scroll(self, height):
        self.browser.execute_script('window.scrollTo(0, {});'.format(height))

    def scroll_to_bottom(self):
        """
        Function for scrolling down the page to the very bottom, need to do this for some websites like Pinterest and
        Linkedin.
        TODO: Need to come up a better solution.
        """
        current_height = self._get_current_height()

        for i in range(0, self.config['max_scroll_times']):
            self.scroll(self._get_current_height())
            sleep(self.config['scroll_pause_time'])
            new_height = self._get_current_height()

            if new_height == current_height:
                break

            current_height = new_height
