from logging_module import Logger
from random import randint


class ProxyPool(object):

    def __init__(self, *proxies):
        self.logger = Logger.get_logger()
        self.proxies = []

        for proxy in proxies:
            self.add_proxy(proxy)

    def add_proxy(self, proxy):
        if proxy.is_alive():
            self.proxies.append(proxy)
        else:
            self.logger.error('Proxy {} is dead'.format(proxy))

    def remove_dead(self):
        self.proxies = [proxy for proxy in self.proxies if proxy.is_alive()]

    def get_random_proxy(self):
        return self.proxies[randint(0, len(self.proxies) - 1)]
