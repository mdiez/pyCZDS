import unittest

from src.pyczds.client import CZDSClient


class TestPyCZDS(unittest.TestCase):
    def setUp(self):
        # In order to run these tests, enter your valid username and password for the CZDS website here.
        # Please note that these tests do not change any data.

        # TODO PASTE USERNAME AND PASSWORD HERE
        username = ''
        password = ''
        # END TODO

        if not username or not password:
            raise Exception('Please set username and password in tests/test_pyczds.py before running it.')

        self.username = username
        self.password = password

        self.client = CZDSClient(username=username, password=password)
        self.test_token = 'eyJraWQiOiJzZEF5bzA4TGpnZU54LWZzcGl3Q3VNTEE5RXRLRmlyX3g2OUFGeEQ5aUtZIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmRIWUw0X1JleTZ1QlE1azUwaTJOYU1Tbk81Tjlkc1pnUExRRU5UQTAya2siLCJpc3MiOiJodHRwczovL2ljYW5uLWFjY291bnQub2t0YS5jb20vb2F1dGgyL2F1czJwMDFjMnJvSkFlQ2dZMnA3IiwiYXVkIjoiaHR0cDovL2FwaV9hdXRoZW5yaXphdGlvbl9zZXJ2ZXIuaWNhbm4ub3JnIiwiaWF0IjoxNjcwNzkzNDc1LCJleHAiOjE2NzA4Nzk4NzUsImNpZCI6IjBvYTFyY2prcWtPbGlNUHVMMnA3IiwidWlkIjoiMDB1N2N5MXJqaktGbG01cW4ycDciLCJzY3AiOlsiaWNhbm4tY3VzdG9tIiwib3BlbmlkIl0sImF1dGhfdGltZSI6MTY3MDc5MzQ3NSwic3ViIjoidGVzdC1weWNkenNAZXhhbXBsZS5jb20iLCJnaXZlbl9uYW1lIjoiVGVzdCIsImZhbWlseV9uYW1lIjoiUHlDRFpTIiwiZW1haWwiOiJ0ZXN0LXB5Y2R6c0BleGFtcGxlLmNvbSJ9.A8_qsWDBy0vJGVv2a3Q64JTDYzxicdL0BdNsrl4dnQmYWhmwrJ7aAyNbmvWtBfd9_XhSswJUwZl9B61ANW-xpu5TSfUGF0R_2AWQ2ppzB2UUNUkCyetnfzd3LVwDXb6vqoEQLRAuVgAgxEOpwdCKlqNgsujWRg2e38w9qCtRAaiFTO8BvZ0eA_vo2zfWGnR6lo27J9ElWTUejZWBC1wzzwN60pZyjT3yJDfjBo4b8plXjKgtibyErWUdpOyCkhHbN6UFEyvfxyril6R8AZ8bWS5lzTmlvw_2yd9TG1xZA7hE9qbQJVK7ymslsOi7LFDSglcVa1vc6V0r1SCDH_k4Ig'
