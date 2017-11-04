from exceptions import QueueEmpty


class BaseQueue(object):

    def __init__(self, timeout=None, **config):
        self._timeout = timeout
        self._config = config

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.get()
        except QueueEmpty:
            raise StopIteration

    def get(self):
        pass
