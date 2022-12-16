import base64
import json

from requests import HTTPError

from src.pyczds.client import CZDSClient
from test_pyczds import TestPyCZDS


class TestAuthentication(TestPyCZDS):
    # region offline tests
    def test_instantiate_client_no_username(self):
        # Client should raise ValueError if username is empty.
        with self.assertRaises(ValueError):
            CZDSClient(username='', password='password')

    def test_instantiate_client_invalid_username(self):
        # Client should raise ValueError if username is not an email address.
        with self.assertRaises(ValueError):
            CZDSClient(username='user', password='password')

    def test_instantiate_client_no_password(self):
        # Client should raise ValueError if password is empty.
        with self.assertRaises(ValueError):
            client = CZDSClient(username='test@test.com', password='')

    def test_jwt_payload_returned_offline(self):
        # Client should return the payload in the JWT portion of the token.
        self.client._token = self.test_token
        j = self.client._get_token_jwt_payload()

        payload_b64 = self.test_token.split('.')[1]
        s = base64.b64decode(payload_b64)
        j_reference = json.loads(s)

        self.assertEqual(j, j_reference)

    def test_jwt_payload_raises_empty_token(self):
        # If token is empty, method should raise a ValueError.
        self.client._token = str()
        with self.assertRaises(ValueError):
            j = self.client._get_token_jwt_payload()

    def test_not_authenticated_token_empty(self):
        # Client is should not be authenticated if there's no token saved.
        self.client._token = ''
        self.assertFalse(self.client._is_authenticated())

    def test_not_authenticated_token_expired(self):
        # Client should not be authenticated if token has expired.
        self.client._token = self.test_token
        self.assertFalse(self.client._is_authenticated())
    # endregion

    # region online tests
    def test_authenticate_invalid_username_online(self):
        # Client should raise an HTTPError if authentication is unsuccessful.
        self.client._username = 'invalid_user_pycdzs'
        self.client._password = 'invalid_password_pycdzs'

        with self.assertRaisesRegex(HTTPError, '.*nvalid credentials provided.*'):
            self.client._authenticate()

    def test_authenticate_invalid_password_online(self):
        # Client should raise an HTTPError if authentication is unsuccessful.
        self.client._username = self.username
        self.client._password = 'invalid_password_pycdzs'

        # There seems to be a bug in the API. If the username is correct, but the password is wrong,
        # instead of status code 401 (Invalid credentials), status code 400 ("Request is malformed") is returns.
        with self.assertRaisesRegex(HTTPError, '.*equest.*malformed.*'):
            self.client._authenticate()

    def test_authenticate_valid_username_password_online(self):
        # Client should be authenticated if username and password are correct.
        self.client._username = self.username
        self.client._password = self.password

        self.client._authenticate()
        self.assertTrue(self.client._is_authenticated())

    def test_jwt_payload_returned_online(self):
        # Client should return the payload in the JWT portion of the token.
        self.client._authenticate()
        j = self.client._get_token_jwt_payload()
        self.assertEqual(j['sub'], self.client._username)

    # endregion
