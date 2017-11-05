from exceptions import InvalidParam
from bs4 import BeautifulSoup


class BaseCrawler(object):

    """
    Base class for crawlers
    """

    DEFAULT_CONFIG = {}

    def __init__(self, **config):
        self._selector = {}
        self._proxies = None

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        self._proxies = proxies

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, pattern):
        # Add more validation
        if isinstance(pattern, str):
            self._selector = pattern
        else:
            raise InvalidParam('selector should be in a valid css selector format')

    def crawl(self, url):
        pass

    def auth(self, **auth):
        pass

    def _parse_markup(self, markup):
        parsed = BeautifulSoup(markup, 'html5lib')
        matched = parsed.select(self.selector)
        return [ele for ele in matched]

    def _parse_config(self, config):
        parsed_settings = self.DEFAULT_CONFIG

        for param, setting in config.items():
            if param not in self.DEFAULT_CONFIG:
                raise InvalidParam('Unknown parameter {}.'.format(param))
            elif not isinstance(setting, type(self.DEFAULT_CONFIG[param])):
                raise InvalidParam('Invalid setting {} for {}.'.format(setting, param))

            parsed_settings[param] = setting

        return parsed_settings
