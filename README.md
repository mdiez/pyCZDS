# pyCZDS – An API client for ICANN's Centralized Zone Data Service (CZDS)

This repository hosts the source code for the respective Python package which can be found on [PyPI]().

## Installation

This package requires Python 3 and has been tested with Python 3.10.8. It requires the `requests` package.
The library implements a client against the official API documentation which can be found under this [link](https://github.com/icann/czds-api-client-java/blob/master/docs/ICANN_CZDS_api.pdf).

Install pyCZDS with the command `pip install pyCZDS`.

## Usage
The library supports the following actions:
* `client.get_zone_download_links` – retrieves the download links all zonefiles the respective account is authorized to access;
* `client.head_zonefile` – retrieves the headers for a specified zonefile, which contain metadata such as the last modified timestamp and the file's size;
* `client.download_zonefile` – download a specified zonefile.

### Instantiating a client
Use the following code to create a new `CZDSClient` object:
```
from pyczds.client import CZDSClient

# replace username and password with actual credentials
c = CZDSClient(username, password)
```

The client handles the authentication with the API transparently. It will authenticate with the first call of any method, and will retain the acquired token for subsequent requests. When the token expires, it will renew the authentication automatically.

### Getting zonefile download links
The following command will retrieve a list of all zonefiles the account is authorized to access. It returns a `list` with the respective URLs.

```
print(c.get_zone_download_links())
# [
    'https://czds-download-api.icann.org/czds/downloads/net.zone',
    ...
    'https://czds-download-api.icann.org/czds/downloads/com.zone'
]
```
Requests for accessing additional zonefiles can be made online under this [link](https://czds.icann.org/zone-request/add).

### Requesting the headers for a zonefile
The following command will retrieve the headers for a specified zonefile. It returns a `dict`:
```
print(c.head_zonefile('https://czds-download-api.icann.org/czds/downloads/vision.zone'))
# {
    'Date': 'Fri, 16 Dec 2022 19:42:58 GMT',
    ...
    'Last-Modified': 'Fri, 16 Dec 2022 01:29:08 GMT',
    ...
    'Content-Disposition': 'attachment;filename=vision.txt.gz',
    ...
    'Content-Length': '602034',
    ...
}
```

### Downloading a zonefile
The following command will download a specified zonefile to your computer:
```
c.get_zonefile('https://czds-download-api.icann.org/czds/downloads/vision.zone', download_dir='zonefiles/')
```
The parameter `download_dir` is optional. If it is not passed, the file will be downloaded to the working directory of your script.


## Troubleshooting
Should you encounter errors, a good first step is to increase the logging level to `debug` and then analyze the output.

```
import logging

from pycdzs import client

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Run the problematic command
c = client.CZDSClient(username, password)
```

## Tests
The entire codebase is covered. Run the test from the `tests` directory. Before you do so, make sure you set `username` and `password` in `tests/test_pyczds.py`: 

```
class TestPyCZDS(unittest.TestCase):
    def setUp(self):
        # In order to run these tests, enter your valid username and password for the CZDS website here.
        # Please note that these tests do not change any data.

        # TODO PASTE USERNAME AND PASSWORD HERE
        username = ''
        password = ''
        # END TODO
```

## Legal disclaimer
I am a hobby enthusiast and am neither affiliated with ICANN, nor is this library endorsed by ICANN.

## Links and further information
* [CDZS – Login](https://czds.icann.org/)
* [CZDS – Help](https://czds.icann.org/help)
* [CZDS – Request access to additional hostfiles](https://czds.icann.org/zone-request/add)