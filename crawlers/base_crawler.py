from exceptions import InvalidParamException


class BaseCrawler(object):

    """
    Base class for crawlers
    """

    DEFAULT_CONFIG = {}

    def __init__(self, timeout=None, **kwargs):
        pass

    def set_selector(self, pattern):
        pass

    def crawl(self, url):
        pass

    def auth(self):
        pass

    def _parse_config(self, config):
        parsed_settings = self.DEFAULT_CONFIG

        for param, setting in config.items():
            if param not in self.DEFAULT_CONFIG:
                raise InvalidParamException('Unknown parameter {}.'.format(param))
            elif not isinstance(setting, type(self.DEFAULT_CONFIG[param])):
                raise InvalidParamException('Invalid setting {} for {}.'.format(setting, param))

            parsed_settings[param] = setting

        return parsed_settings
