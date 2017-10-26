class BaseCrawler(object):

    """
    Base class for crawlers
    """

    def __init__(self, timeout=None, **kwargs):
        pass

    def set_selector(self, pattern):
        pass

    def crawl(self, url):
        pass
