from .base_queue import BaseQueue
from queue import Queue, Empty
from exceptions import QueueEmpty


class DefaultQueue(BaseQueue):

    def __init__(self, timeout=None, **config):
        self._queue = Queue()
        super(DefaultQueue, self).__init__(timeout, **config)

    def get(self):
        try:
            return self._queue.get(timeout=self._timeout)
        except Empty:
            raise QueueEmpty('No more jobs in this queue.')
