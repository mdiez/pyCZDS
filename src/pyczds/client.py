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

    def _do_request(self, method, url, stream=False):
        if not self._is_authenticated():
            logging.debug('Not authenticated. Attempting authentication.')
            self._authenticate()

        headers = {
            'Authorization': 'Bearer {}'.format(self._token),
            'User-Agent': '{} / {}'.format(
                metadata.distribution('pyCZDS').name, metadata.distribution('pyCZDS').version
            )
        }

        request = requests.Request(method.upper(), url=url, headers=headers)
        prepared_request = request.prepare()
        self._preprocess_request(prepared_request)

        response = requests.Session().send(prepared_request, stream=stream)
        self._preprocess_response(response, stream)

        return response

    def get_zone_download_links(self):
        logging.debug('About to request zonefile links list.')

        link_list = self._do_request('get', self.ZONE_DOWNLOAD_LINKS_LIST_URL).json()

        if len(link_list) == 0:
            raise Exception('This account does not seem to have access to any zonefiles.')

        return link_list

    def head_zonefile(self, zonefile_link):
        logging.debug('About to request headers for zonefile {}.'.format(zonefile_link.split('/')[-1]))

        headers = self._do_request('head', zonefile_link).headers

        return headers

    def get_zonefile(self, zonefile_link, download_dir='', filename=''):
        if not download_dir or (download_dir and len(download_dir) == 0):
            download_dir = os.getcwd()

        url_parsed = urlparse(zonefile_link)
        remote_filename = unquote(os.path.basename(url_parsed.path))

        logging.debug('About to start download for zonefile {} to directory {}.'.format(
            remote_filename, download_dir)
        )

        with self._do_request('get', zonefile_link, stream=True) as response:
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

            filepath = os.path.join(download_dir, filename)

            logging.debug('Streaming file to {}.'.format(filepath))

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=2**19):
                    f.write(chunk)

            logging.debug('Completed download of zonefile {}.'.format(filepath))
