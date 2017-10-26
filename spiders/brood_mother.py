from .exceptions import InvalidParamException


class BroodMother(object):

    """
    deepest_crawl_level: deepest level that the crawler will go
    crawl_mode:
        human: slowest, uses selenium with PhantomJS to mock user actions.
        normal: single thread requests with random intervals in between requests.
        faster: multi-thread requests with random intervals in between requests.
        fastest: multi-thread requests without any interval in between requests.
        distributed: will implement this later, was thinking to use celery and rabbit-mq.
    max_waiting: maximum waiting time in between requests (seconds).
    min_waiting: minimum waiting time in between requests (seconds).
    max_threads: maximum threads will be used for crawling, will not be available in distributed mode.
    """

    DEFAULT_CONFIG = {
        'deepest_crawl_level': 2,
        'crawl_mode': 'normal',
        'max_waiting': 5,
        'min_waiting': 2,
        'max_threads': 1,
        'enable_cookie': False
    }

    AVAILABLE_MODES = ['human', 'normal', 'faster', 'fastest']

    def __init__(self, start_url, **kwargs):
        self.start_url = start_url
        self.config = self._parse_config(kwargs)

    def _parse_config(self, config):
        parsed_settings = self.DEFAULT_CONFIG

        for param, setting in config.items():
            if param not in self.DEFAULT_CONFIG:
                raise InvalidParamException('Unknown spider config {}.'.format(param))
            elif param == 'crawl_mode' and setting not in self.AVAILABLE_MODES:
                raise InvalidParamException('Unknown crawl mode {}.'.format(setting))
            elif not isinstance(setting, type(self.DEFAULT_CONFIG[param])):
                raise InvalidParamException('Invalid setting {} for {}.'.format(setting, param))

            parsed_settings[param] = setting

        return parsed_settings
