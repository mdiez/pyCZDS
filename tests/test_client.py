import random
import logging
import os
import tempfile
import cgi

from test_pyczds import TestPyCZDS


class TestClient(TestPyCZDS):

    # region online tests
    def test_get_zone_download_links_online(self):
        zonefile_link_list = self.client.get_zone_download_links()
        self.assertTrue(isinstance(zonefile_link_list, list))

    def test_head_zonefile_online(self):
        zonefile_link_list = self.client.get_zone_download_links()
        link = random.choice(zonefile_link_list)

        head = self.client.head_zonefile(link)

        self.assertGreater(len(head), 0)
        self.assertIn('date', head)
        self.assertIn('server', head)
        self.assertIn('last-modified', head)
        self.assertGreater(int(head['content-length']), 0)
        self.assertEqual(head['content-type'], 'application/x-gzip')

    def download_smallest_zonefile(self, download_dir='', filename=''):
        zonefile_link_list = self.client.get_zone_download_links()
        smallest_file_size = int()
        smallest_file_url = str()
        smallest_file_filename = str()

        for link in zonefile_link_list:
            head = self.client.head_zonefile(link)
            if smallest_file_size == 0 or int(head['Content-Length']) < smallest_file_size:
                value, params = cgi.parse_header(head['Content-Disposition'])
                smallest_file_size = int(head['Content-Length'])
                smallest_file_url = link
                smallest_file_filename = params['filename']

        logging.debug(
            'Identified {} as smallest file with {} bytes to download.'.format(smallest_file_url, smallest_file_size)
        )

        if len(filename) > 0:
            local_filename = filename
        else:
            local_filename = smallest_file_filename

        self.client.get_zonefile(smallest_file_url, download_dir, local_filename)

        if len(download_dir) > 0:
            filepath = os.path.join(download_dir, local_filename)
        else:
            filepath = os.path.join(os.getcwd(), local_filename)

        filesize = os.stat(filepath)

        self.assertEqual(smallest_file_size, filesize.st_size)

        logging.debug('Removing downloaded file {} from {}.'.format(local_filename, filepath))

        os.remove(filepath)

    def test_download_smallest_zonefile_default_directory_online(self):
        self.download_smallest_zonefile()

    def test_download_smallest_zonefile_other_filename_online(self):
        with tempfile.TemporaryDirectory() as d:
            self.download_smallest_zonefile(filename='test_zonefile.tmp')

    def test_download_smallest_zonefile_other_directory_online(self):
        with tempfile.TemporaryDirectory() as d:
            self.download_smallest_zonefile(d)

    def test_download_smallest_zonefile_other_directory_other_filename_online(self):
        with tempfile.TemporaryDirectory() as d:
            self.download_smallest_zonefile(d, 'test_zonefile.tmp')

    # endregion
