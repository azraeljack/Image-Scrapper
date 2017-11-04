import logging
from exceptions import InvalidParam


class Logger(object):
    class __LoggerInstance(object):
        def __init__(self, log_type, log_path, log_level, log_format):
            self._logger = logging.getLogger('image_scrapper')
            self._logger.setLevel(log_level)
            self._logger.addHandler(self.get_handler(log_type, log_path, log_level, log_format))

        def get_logger(self):
            return self._logger

        @staticmethod
        def get_handler(log_type, log_path, log_level, log_format):
            if log_type == 'console':
                handler = logging.StreamHandler()
            elif log_type == 'file':
                handler = logging.FileHandler(log_path if log_path else 'crawler.log')
            else:
                raise InvalidParam('Unknown logging type {}'.format(log_type))

            handler.setLevel(log_level)
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' if not log_format else log_format
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

            return handler

    instance = None

    def __init__(self, log_type, log_path=None, log_level='INFO', log_format=None):
        if not Logger.instance:
            Logger.instance = Logger.__LoggerInstance(log_type, log_path, log_level, log_format)

    def __getattr__(self, item):
        return getattr(self.instance, item)
