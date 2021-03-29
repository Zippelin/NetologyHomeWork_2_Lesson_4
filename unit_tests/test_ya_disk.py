import requests
import time
from urllib.parse import urljoin
import pytest


class TestYaDiskAPI:
    __BASE_URL = 'https://cloud-api.yandex.net'
    __ENDPOINT_DIR = 'v1/disk/resources'
    __token = ''
    __TOKEN_FILE_PATH = 'token.txt'
    __test_dir = ''

    def setup_class(self):
        self.__test_dir = 'test_dir' + str(time.time())
        with open(self.__TOKEN_FILE_PATH, 'r') as f:
            self.__token = 'OAuth ' + f.readline()

    @pytest.mark.parametrize('method, response_code', (
                    ['PUT', 201],
                    ['GET', 200],
                    ['DELETE', 204]
                )
            )
    def test_resources(self, method, response_code):
        result = requests.request(method=method, url=urljoin(self.__BASE_URL, self.__ENDPOINT_DIR),
                                  params={
                                      'path': self.__test_dir
                                  },
                                  headers={
                                      'Authorization': self.__token
                                  })
        assert result.status_code == response_code, f'Ошибка ответа метода {method} :: {result.status_code}'
