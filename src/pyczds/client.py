import sys
import logging
import cgi
import os
from urllib.parse import urljoin, urlparse, unquote
from importlib import metadata

import requests

from .authentication import CZDSAuthentication


class CZDSClient(CZDSAuthentication):
    BASE_URL = 'https://czds-api.icann.org'
    ZONE_DOWNLOAD_LINKS_LIST_URL = urljoin(BASE_URL, '/czds/downloads/links')

    def __init__(self, username, password):
        super().__init__(username=username, password=password)

        if 'unittest' not in sys.modules.keys():
            self._user_agent = '{} / {}'.format(
                metadata.distribution('pyCZDS').name, metadata.distribution('pyCZDS').version
            )
        else:
            self._user_agent = 'pyCZDS / test'

    def _do_request(self, method, url, stream=False):
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

    def get_zonefiles_list(self):
        logging.debug('About to request zonefile URLs list.')

        url_list = self._do_request('get', self.ZONE_DOWNLOAD_LINKS_LIST_URL).json()

        if len(url_list) == 0:
            raise Exception('This account does not seem to have access to any zonefiles.')

        return url_list

    def head_zonefile(self, zonefile_url):
        logging.debug('About to request headers for zonefile {}.'.format(zonefile_url.split('/')[-1]))

        headers = self._do_request('head', zonefile_url).headers

        return headers

    def get_zonefile(self, zonefile_url, download_dir='', filename=''):
        if not download_dir or (download_dir and len(download_dir) == 0):
            download_dir = os.getcwd()

        url_parsed = urlparse(zonefile_url)
        remote_filename = unquote(os.path.basename(url_parsed.path))

        logging.debug('About to start download for zonefile {} to directory {}.'.format(
            remote_filename, download_dir)
        )

        with self._do_request('get', zonefile_url, stream=True) as response:
            value, params = cgi.parse_header(response.headers['Content-Disposition'])
            if value.lower() != 'attachment':
                raise ValueError(
                    'Received unexpected value in Content-Disposition header: {}.'.format(
                        response.headers['Content-Disposition'])
                )

            if not filename or (filename and len(filename) == 0):
                if 'filename' not in params.keys():
                    raise ValueError(
                        'No filename passed in Content-Disposition header: {}.'.format(
                            response.headers['Content-Disposition'])
                    )

                local_filename = params['filename']
            else:
                local_filename = filename

            filepath = os.path.join(download_dir, local_filename)

            logging.debug('Streaming file to {}.'.format(filepath))

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=2**19):
                    f.write(chunk)

            logging.debug('Completed download of zonefile {}.'.format(filepath))
