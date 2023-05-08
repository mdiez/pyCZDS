# pyCZDS – An API client for ICANN's Centralized Zone Data Service (CZDS)

*This package allows you to seamlessly interact with ICANN's CZDS and download zone files for participating Top-Level Domains.*

> The Centralized Zone Data Service (CZDS) is an online portal where any interested party can request access to the Zone Files provided by participating generic Top-Level Domains (gTLDs).

[Source](https://czds.icann.org/home)

Relevant links:
* [ICANN CZDS homepage](https://czds.icann.org/home)
* pyCZDS on [PyPI](https://pypi.org/project/pyCZDS/)
* pyCZDS repo on [GitHub](https://github.com/mdiez/pyCZDS)

## Installation

This package requires Python 3 and has been tested with Python 3.10.8. It requires the `requests` package.
The library implements a client against the official API documentation which can be found under this [link](https://github.com/icann/czds-api-client-java/blob/master/docs/ICANN_CZDS_api.pdf).

Install pyCZDS with the command `pip install pyCZDS`.

## Usage
The library supports the following actions:
* `client.get_zonefiles_list` – retrieves the download links all zone files the respective account is authorized to access;
* `client.head_zonefile` – retrieves the headers for a specified zone file, which contain metadata such as the last modified timestamp and the file's size;
* `client.get_zonefile` – download a specified zone file.

### Instantiating a client
Use the following code to create a new `CZDSClient` object:
```
from pyczds.client import CZDSClient

# replace username and password with actual credentials
c = CZDSClient(username, password)
```

The client handles the authentication with the API transparently. It will authenticate with the first call of any method, and will retain the acquired token for subsequent requests. When the token expires, it will renew the authentication automatically.

### Getting zone file download URLs
The following command will retrieve a list of all zone files the account is authorized to access. It returns a `list` with the respective URLs.

```
print(c.get_zonefiles_list())
# [
    'https://czds-download-api.icann.org/czds/downloads/net.zone',
    ...
    'https://czds-download-api.icann.org/czds/downloads/com.zone'
]
```
Access to additional zone files can be requested online under this [link](https://czds.icann.org/zone-request/add).

### Requesting the headers for a zone file
Using one of the links received via `get_zonefiles_list()`, the following command retrieves the headers for a specified zonefile. It returns a `dict` (more specifically, a `requests.models.CaseInsensitiveDict`):
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
To facilitate further work with the metadata, the dictionary not only contains the raw HTTP headers, but also a subdict `parsed` (which is a `requests.models.CaseInsensitiveDict`, too), which contains a number of headers parsed in suitable data types:
```
print(c.head_zonefile('https://czds-download-api.icann.org/czds/downloads/vision.zone'))
# {
    'Last-Modified': 'Sat, 17 Dec 2022 00:17:25 GMT',
    'Content-Disposition': 'attachment;filename=net.txt.gz',
    'Content-Length': '481167941',
    ...
    'parsed': {
        'last-modified': datetime.datetime(2022, 12, 17, 0, 17, 25, tzinfo=datetime.timezone.utc),  # datetime
        'content-length': 481167941,  # int
        'filename': 'net.txt.gz'  # string
    }
}
```

### Downloading a zone file
The following command will download a specified zone file:
```
c.get_zonefile('https://czds-download-api.icann.org/czds/downloads/vision.zone', download_dir='zonefiles/', filename='vision_zonefile')
```
Both parameters are optional.
* `download_dir` sets the local directory where the file should be downloaded to. If it is not passed, the file will be downloaded to the working directory of your script.
* `filename` sets the local filename of the downloaded file. If it is not passed, the filename will be set according to the value the API provides in the `Content-Disposition` header, e.g., `vision.tar.gz`.


## Troubleshooting
Should you encounter any errors, a good first step is to increase the logging level to `debug` and then analyze the output.

```
import logging

from pyczds import client

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
* [Wikipedia – Zone file](https://en.wikipedia.org/wiki/Zone_file)
* [CZDS – Login](https://czds.icann.org/)
* [CZDS – Help](https://czds.icann.org/help)
* [CZDS – Request access to additional hostfiles](https://czds.icann.org/zone-request/add)
