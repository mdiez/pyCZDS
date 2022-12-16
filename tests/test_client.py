import random
import logging
import os
import tempfile

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

    def download_smallest_zonefile(self, download_dir=''):
        zonefile_link_list = self.client.get_zone_download_links()
        smallest_file = tuple()

        for link in zonefile_link_list:
            head = self.client.head_zonefile(link)
            if len(smallest_file) == 0 or smallest_file[0] > int(head['Content-Length']):
                smallest_file = (int(head['Content-Length']), link, head['Content-Disposition'].split('=')[1])

        logging.debug(
            'Identified {} as smallest file with {} bytes to download.'.format(smallest_file[0], smallest_file[2])
        )

        self.client.get_zonefile(smallest_file[1], download_dir)

        if download_dir == '':
            filepath = os.path.join(os.getcwd(), smallest_file[2])
        else:
            filepath = os.path.join(download_dir, smallest_file[2])

        filesize = os.stat(filepath)

        self.assertEqual(smallest_file[0], filesize.st_size)

        logging.debug('Removing downloaded file from {}.'.format(filepath))

        os.remove(filepath)

    def test_download_smallest_zonefile_default_directory_online(self):
        self.download_smallest_zonefile()

    def test_download_smallest_zonefile_other_directory_online(self):
        with tempfile.TemporaryDirectory() as d:
            self.download_smallest_zonefile(d)

    # endregion
