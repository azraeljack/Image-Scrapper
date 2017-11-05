from .utils import check_proxy


class Proxy(object):

    def __init__(self, address, port=None, timeout=10):
        self.address = address
        self.timeout = timeout

        if ':' in self.address:
            self.address, port = self.address.split(':')
        elif ':' not in address and not port:
            port = 80

        self.port = int(port)

    def __str__(self):
        return '{}:{}'.format(self.address, self.port)

    def is_alive(self):
        return check_proxy(str(self), self.timeout)['is_alive']

    def get_delay(self):
        return check_proxy(str(self), self.timeout)['delay']
