import logging
import re
import os
from typing import Match

import requests


class CZDSHelpers(object):

    def _is_email_address(self, address_string: str) -> Match:
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(pat, address_string)

    def _preprocess_request(self, request: requests.Request) -> None:
        logging.debug(
            'About to send {} request to URL {} with headers {} and body {}.'.format(
                request.method, request.url, request.headers, str(request.body)
            )
        )

    def _preprocess_response(self, response: requests.Response, stream: bool = False) -> None:
        logging.debug('Returned status code {}.'.format(response.status_code))
        logging.debug('Received headers {}.'.format(response.headers))

        if not stream:
            logging.debug('Received raw response {}.'.format(response.text))

        if response.status_code != 200:
            logging.error('Error during request to API. Returned status code {}.'.format(response.status_code))
            if response.status_code == 400:
                raise requests.HTTPError('Request is malformed.')
            if response.status_code == 401:
                raise requests.HTTPError('Invalid credentials provided, or no valid bearer token provided.')
            if response.status_code == 403:
                raise requests.HTTPError(
                    'Requested zone does not exist, or authenticated user does not have access to the zone.'
                )
            if response.status_code == 409:
                raise requests.HTTPError(
                    'The authenticated user has not accepted the new T&Cs. Please log in to the portal, and accept the T&Cs.'
                )
            if response.status_code == 415:
                raise requests.HTTPError('Unsupported content type header sent.')
            if response.status_code == 429:
                raise requests.HTTPError('Too many authentication attempts from the same IP address.')
            if response.status_code == 500:
                raise requests.HTTPError('Internal service error.')

    def _check_file_size(self, file_path: str, size: int) -> None:
        file_size = os.path.getsize(file_path)

        if file_size != size:
            raise Exception(
                'The size of the file ({:,} bytes) differs from the size announced in the header ({:,} bytes).'.format(
                    file_size, size
                )
            )
