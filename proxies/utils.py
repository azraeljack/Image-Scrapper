import requests
from time import time


def check_proxy(proxy, timeout):
    """
    Just a basic function for testing if the proxy is still alive, might need to come up a better idea instead of
    requesting google every time.
    :param proxy: a proxy string looks like '192.168.0.1:8080'
    :param timeout: test timeout in seconds
    :return: a dictionary shows delay in ms and status of the proxy
    :rtype: dict
    """

    try:
        start_time = int(time() * 1000)
        resp = requests.get('https://www.google.com', proxies={'https': proxy}, timeout=timeout)

        if resp.status_code == requests.codes.ok:
            end_time = int(time() * 1000)
            time_used_ms = end_time - start_time
            return {'delay': time_used_ms, 'is_alive': True}
    finally:
        return {'delay': None, 'is_alive': False}
