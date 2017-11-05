from crawlers.base_crawler import BaseCrawler
from logging_module import Logger
from exceptions import InvalidParam
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from random import uniform


class SeleniumCrawler(BaseCrawler):
    DEFAULT_CONFIG = {
        'web_driver': 'phantomjs',
        'executable_path': '../resource/phantomjs/phantomjs',
        'scroll_to_bottom': False,
        'page_timeout': 10,
        'max_scroll_pause_time': 1.5,
        'min_scroll_pause_time': 1,
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
        self.logger = Logger().get_logger()
        self.config = self._parse_config(config)
        driver_class = self.WEB_DRIVERS[self.config.get('web_driver', 'phantomjs').lower()]

        executable_path = self.config.get('executable_path')

        if not executable_path:
            raise InvalidParam('Invalid executable path provided.')

        self.browser = driver_class(executable_path)
        super(SeleniumCrawler, self).__init__(**config)

    def _get_current_height(self):
        height = self.browser.execute_script('return document.body.scrollHeight;')
        self.logger.debug('Current height is {}'.format(height))
        return height

    def crawl(self, url, wait_until='body'):
        self.logger.info('Loading url {} ...'.format(url))
        self.browser.get(url)
        WebDriverWait(self.browser, self.config['page_timeout']).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, wait_until))
        )

        if self.config.get('scroll_to_bottom'):
            self.logger.debug('Scrolling down page to the very bottom...')
            self.scroll_to_bottom()

        return self._parse_markup(self.browser.page_source)

    def scroll(self, height):
        self.logger.debug('Scrolling page to {}...'.format(height))
        self.browser.execute_script('window.scrollTo(0, {});'.format(height))

    def scroll_to_bottom(self):
        """
        Function for scrolling down the page to the very bottom, need to do this for some websites like Pinterest and
        Linkedin.
        TODO: Need to come up a better solution.
        """
        current_height = self._get_current_height()
        max_pause = self.config['max_scroll_pause_time']
        min_pause = self.config['min_scroll_pause_time']

        for i in range(0, self.config['max_scroll_times']):
            self.scroll(self._get_current_height())

            pause = uniform(min_pause, max_pause)
            self.logger.debug('Too much scrolling, take a rest for {} seconds'.format(pause))
            sleep(pause)

            new_height = self._get_current_height()

            if new_height == current_height:
                self.logger.debug('Reached the bottom of the page')
                break

            current_height = new_height


if __name__ == '__main__':
    Logger('console', log_level='DEBUG')
    sc = SeleniumCrawler(scroll_to_bottom=True)
    sc.selector = {'name': 'img'}
    elements = sc.crawl('https://www.pinterest.ca/search/pins/?q=%E7%AA%97%E5%B8%98')
    for element in elements:
        print(element['src'])

    print('Total {} links crawled!'.format(len(elements)))
