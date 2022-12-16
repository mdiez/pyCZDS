from requests import HTTPError

from test_pyczds import TestPyCZDS


class MockRequest(object):
    def __init__(self, status_code=200, headers='', text=''):
        self.status_code = status_code
        self.headers = headers
        self.text = text


class TestHelpers(TestPyCZDS):
    # region offline tests
    def test_http_status_400(self):
        r = MockRequest(400)
        with self.assertRaisesRegex(HTTPError, '.malformed.'):
            self.client._preprocess_response(r)

    def test_http_status_401(self):
        r = MockRequest(401)
        with self.assertRaisesRegex(HTTPError, '.nvalid credentials.*no valid bearer token.'):
            self.client._preprocess_response(r)

    def test_http_status_403(self):
        r = MockRequest(403)
        with self.assertRaisesRegex(HTTPError, '.*zone.*not exist.*not have access*'):
            self.client._preprocess_response(r)

    def test_http_status_409(self):
        r = MockRequest(409)
        with self.assertRaisesRegex(HTTPError, '.T\&Cs.'):
            self.client._preprocess_response(r)

    def test_http_status_415(self):
        r = MockRequest(415)
        with self.assertRaisesRegex(HTTPError, '.nsupported content type.'):
            self.client._preprocess_response(r)

    def test_http_status_429(self):
        r = MockRequest(429)
        with self.assertRaisesRegex(HTTPError, '.oo many authentication attempts.'):
            self.client._preprocess_response(r)

    def test_http_status_500(self):
        r = MockRequest(500)
        with self.assertRaisesRegex(HTTPError, '.nternal service error.'):
            self.client._preprocess_response(r)
    # endregion
