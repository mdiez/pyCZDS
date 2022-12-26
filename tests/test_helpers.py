import tempfile
import os

from requests import HTTPError

from test_pyczds import TestPyCZDS


class MockRequest(object):
    def __init__(self, status_code=200, headers='', text=''):
        self.status_code = status_code
        self.headers = headers
        self.text = text


class TestHelpers(TestPyCZDS):
    # region offline tests
    def test_http_status_400_offline(self):
        r = MockRequest(400)
        with self.assertRaisesRegex(HTTPError, '.malformed.'):
            self.client._preprocess_response(r)

    def test_http_status_401_offline(self):
        r = MockRequest(401)
        with self.assertRaisesRegex(HTTPError, '.nvalid credentials.*no valid bearer token.'):
            self.client._preprocess_response(r)

    def test_http_status_403_offline(self):
        r = MockRequest(403)
        with self.assertRaisesRegex(HTTPError, '.*zone.*not exist.*not have access*'):
            self.client._preprocess_response(r)

    def test_http_status_409_offline(self):
        r = MockRequest(409)
        with self.assertRaisesRegex(HTTPError, '.T\&Cs.'):
            self.client._preprocess_response(r)

    def test_http_status_415_offline(self):
        r = MockRequest(415)
        with self.assertRaisesRegex(HTTPError, '.nsupported content type.'):
            self.client._preprocess_response(r)

    def test_http_status_429_offline(self):
        r = MockRequest(429)
        with self.assertRaisesRegex(HTTPError, '.oo many authentication attempts.'):
            self.client._preprocess_response(r)

    def test_http_status_500_offline(self):
        r = MockRequest(500)
        with self.assertRaisesRegex(HTTPError, '.nternal service error.'):
            self.client._preprocess_response(r)

    def test_file_size_difference(self):
        test_string = '1234567890'
        test_string_size = len(test_string) - 1

        with tempfile.TemporaryDirectory() as d:
            file_path = os.path.join(d, 'file_size_test.tmp')
            with open(file_path, 'w') as f:
                f.write(test_string)

            with self.assertRaisesRegex(Exception, '.*size of the file.*differs.*'):
                self.client._check_file_size(file_path, test_string_size)

    def test_file_size_identical(self):
        test_string = '1234567890'
        test_string_size = len(test_string)

        with tempfile.TemporaryDirectory() as d:
            file_path = os.path.join(d, 'file_size_test.tmp')
            with open(file_path, 'w') as f:
                f.write(test_string)

            self.client._check_file_size(file_path, test_string_size)

    # endregion
