import logging
import json
import base64
import time

import requests

from .helpers import CZDSHelpers


class CZDSAuthentication(CZDSHelpers):
    AUTH_URL = "https://account-api.icann.org/api/authenticate"

    def __init__(self, username: str, password: str) -> None:
        if not isinstance(username, str) or len(username) == 0 or not self._is_email_address(username):
            raise ValueError('Username invalid.')

        if not isinstance(password, str) or len(password) == 0:
            raise ValueError('Password invalid.')

        self._username = username
        self._password = password

        self._token = str()

    def _get_token_jwt_payload(self) -> json:
        logging.debug('Parsing JWT payload.')

        if len(self._token) == 0:
            raise ValueError('Authentication token is not set.')

        payload_b64 = self._token.split('.')[1]
        s = base64.b64decode(payload_b64 + '=' * (-len(payload_b64) % 4))
        j = json.loads(s)

        logging.debug('JSON content of JWT payload: {}'.format(json.dumps(j)))

        return j

    def _is_authenticated(self) -> bool:
        logging.debug('About to check if client is authenticated or not.')

        if len(self._token) > 0:
            j = self._get_token_jwt_payload()

            if j['exp'] > time.time():
                logging.debug('Token is set and has not yet expired. Client is authenticated.')
                return True

            logging.debug('Not authenticated because token has expired.')

        else:
            logging.debug('Not authenticated because auth token is not set.')

        return False

    def _authenticate(self) -> None:
        logging.debug('About to authenticate with username {}.'.format(self._username))

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        credentials = {
            'username': self._username,
            'password': self._password,
        }

        request = requests.Request(method='POST', url=self.AUTH_URL, data=json.dumps(credentials), headers=headers)
        prepared_request = request.prepare()
        self._preprocess_request(prepared_request)

        response = requests.Session().send(prepared_request)
        self._preprocess_response(response)

        token = response.json()['accessToken']

        logging.debug('Successfully authenticated. Received token {}.'.format(token))

        token_padded = token + '=' * ((4 - len(token) % 4) % 4)
        self._token = token_padded
