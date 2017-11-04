from .base_queue import BaseQueue
from kafka import KafkaConsumer
from kafka.errors import KafkaTimeoutError
from exceptions import QueueEmpty
import json


class KafkaQueue(BaseQueue):

    def __init__(self, timeout=None, broker='localhost:9092', topic='', **config):
        timeout_ms = timeout * 1000 if isinstance(timeout, int) else 40 * 1000
        kafka_config = config.pop('kafka_config', {})
        self._queue = KafkaConsumer(topic, bootstrap_servers=broker, request_timeout_ms=timeout_ms, **kafka_config)
        super(KafkaQueue, self).__init__(timeout, **config)

    def get(self):
        try:
            job = next(self._queue)
            return json.loads(job.value.decode('utf-8'))
        except KafkaTimeoutError:
            raise QueueEmpty('No more jobs in this queue.')
