import sys
import logging
import os
from urllib.parse import urljoin, urlparse, unquote
from email.utils import parsedate_to_datetime
from email.message import EmailMessage

import requests

from .authentication import CZDSAuthentication


class CZDSClient(CZDSAuthentication):
    BASE_URL = 'https://czds-api.icann.org'
    ZONE_DOWNLOAD_LINKS_LIST_URL = urljoin(BASE_URL, '/czds/downloads/links')

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username=username, password=password)

        self._user_agent = '{} / {}'.format('pyCZDS', '1.6')

        if 'unittest' in sys.modules.keys():
            self._user_agent = '{} TEST'.format(self._user_agent)

    def _do_request(self, method: str, url: str, stream: bool = False) -> requests.Response:
        if not self._is_authenticated():
            logging.debug('Not authenticated. Attempting authentication.')
            self._authenticate()

        headers = {
            'Authorization': 'Bearer {}'.format(self._token),
            'User-Agent': self._user_agent
        }

        request = requests.Request(method.upper(), url=url, headers=headers)
        prepared_request = request.prepare()
        self._preprocess_request(prepared_request)

        response = requests.Session().send(prepared_request, stream=stream)
        self._preprocess_response(response, stream)

        return response

    def _parse_headers(self, headers: requests.models.CaseInsensitiveDict) -> requests.models.CaseInsensitiveDict:
        parsed = requests.models.CaseInsensitiveDict()

        parsed['last-modified'] = parsedate_to_datetime(headers['last-modified'])
        parsed['content-length'] = int(headers['content-length'])

        msg = EmailMessage()
        msg['content-disposition'] = headers['content-disposition']
        filename = msg.get_filename()
        parsed['filename'] = filename

        headers['parsed'] = parsed

        return headers

    def get_zonefiles_list(self) -> list:
        logging.debug('About to request zonefile URLs list.')

        url_list = self._do_request('get', self.ZONE_DOWNLOAD_LINKS_LIST_URL).json()

        if len(url_list) == 0:
            raise Exception('This account does not seem to have access to any zonefiles.')

        return url_list

    def head_zonefile(self, zonefile_url: str) -> requests.models.CaseInsensitiveDict:
        logging.debug('About to request headers for zonefile {}.'.format(zonefile_url.split('/')[-1]))

        headers = self._do_request('head', zonefile_url).headers
        headers = self._parse_headers(headers)

        return headers

    def get_zonefile(self, zonefile_url: str, download_dir: str = '', filename: str = '') -> None:
        if not download_dir or (download_dir and len(str(download_dir)) == 0):
            download_dir = os.getcwd()

        url_parsed = urlparse(zonefile_url)
        remote_filename = unquote(os.path.basename(url_parsed.path))

        logging.debug('About to start download for zonefile {} to directory {}.'.format(
            remote_filename, download_dir)
        )

        with self._do_request('get', zonefile_url, stream=True) as response:
            headers = self._parse_headers(response.headers)
            header_size = headers['parsed']['content-length']

            if not filename or (filename and len(filename) == 0):
                local_filename = headers['parsed']['filename']
            else:
                local_filename = filename

            file_path = os.path.join(download_dir, local_filename)

            logging.debug('Streaming file with {:,} bytes to {}.'.format(header_size, file_path))

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=2**19):
                    f.write(chunk)
                    file_size = os.path.getsize(file_path)
                    logging.info(
                        '[{:.0%}] Downloaded {:,} of {:,} bytes.'.format(
                            file_size / header_size, file_size, header_size
                        )
                    )

            logging.debug('Completed download of zonefile {}.'.format(file_path))

            self._check_file_size(file_path, header_size)
