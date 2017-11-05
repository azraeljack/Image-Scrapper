from exceptions import InvalidParam
import metadata


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
        'deepest_crawl_level': 1,
        'crawl_mode': 'normal',
        'max_waiting': 5,
        'min_waiting': 2,
        'max_threads': 1,
        'enable_cookie': False,
        'quality': 'normal'
    }

    AVAILABLE_QUALITIES = ['small', 'normal', 'best']
    AVAILABLE_MODES = ['human', 'normal', 'faster', 'fastest']

    def __init__(self, start_url=None, keyword=None, query_type=None, proxies=None, **kwargs):
        if start_url:
            self.start_url = start_url
        else:
            if not query_type:
                raise InvalidParam('Required start_url if query_type is unknown')
            if not keyword:
                raise InvalidParam('Required keyword if query_type has been specified')

            link = None

            self.start_url = link

        self.config = self._parse_config(kwargs)

    def _parse_config(self, config):
        parsed_settings = self.DEFAULT_CONFIG

        for param, setting in config.items():
            if param not in self.DEFAULT_CONFIG:
                raise InvalidParam('Unknown spider config {}.'.format(param))
            elif param == 'crawl_mode' and setting not in self.AVAILABLE_MODES:
                raise InvalidParam('Unknown crawl mode {}.'.format(setting))
            elif param == 'quality' and setting not in self.AVAILABLE_QUALITIES:
                raise InvalidParam('Unknown image quality {}'.format(setting))
            elif not isinstance(setting, type(self.DEFAULT_CONFIG[param])):
                raise InvalidParam('Invalid setting {} for {}.'.format(setting, param))

            parsed_settings[param] = setting

        return parsed_settings
