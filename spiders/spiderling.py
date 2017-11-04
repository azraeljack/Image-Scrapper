from threading import Thread, get_ident
from requests import Session, status_codes
from logging_module import Logger
from exceptions import InvalidParam
import os


class Spiderling(Thread):

    def __init__(self, queue, quality, output_path, **kwargs):
        self.id = get_ident()
        self.logger = Logger.get_logger()
        self._queue = queue
        self._quality = quality
        self._session = Session()
        self._exit_timeout = kwargs.get('exit_timeout', 3)
        self._waiting_timeout = kwargs.get('waiting_timeout', 2)

        if os.path.isdir(output_path):
            self._output_path = output_path
        else:
            raise InvalidParam('{} is not a valid directory'.format(output_path))

        super(Spiderling, self).__init__(daemon=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()

    def run(self):
        for item in self._queue.get(timeout=self._waiting_timeout):
            self.download(item)

    def download(self, item):
        resp = self._session.get(item['url'], stream=True)

        if resp.status_code == status_codes.codes.ok:
            output_path = os.path.join(self._output_path, '{}.{}'.format(item['title'], item['format']))
            with open(output_path, 'wb') as file:
                for chunk in resp.iter_content(1024):
                    file.write(chunk)
        else:
            self.logger.error('Error happened when downloading item {}'.format(item['url']))
            self.logger.debug(resp.text)

    def stop(self):
        self.logger.info('Worker')
        self.join(timeout=self._exit_timeout)
