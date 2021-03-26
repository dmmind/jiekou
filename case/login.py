import requests
from common.logger import Log
from urllib3.exceptions import InsecureRequestWarning
import unittest


class Jrd():
    # s = requests.session()
    log = Log()

    def __init__(self, s):
        self.s = s

    # def login(self):
    #     url = 'http://192.168.0.21:8084/app/menu/selectAllFunctionMenu/'
    #     header = {
    #         'Content-Type': 'application/json'
    #     }


class Test_query(unittest.TestCase):
    def setUp(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        self.s = requests.session()

    def test01(self):
        self.url = 'http://192.168.0.21:8084/app/menu/selectAllFunctionMenu/'
        r = self.s.get(self.url, headers=self.headers, verify=False)
        result = r.json()
        data = result['data']
        print(data[0])
        self.assertEqual(u'200', result['code'])