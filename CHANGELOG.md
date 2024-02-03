# pyCZDS Changelog

## 1.7.3 (03 February 2024)
### Features
(no changes)

### Tests
(no changes)

### Internals
- Bumped the version number sent in the user agent request header to 1.7

### Documentation
- Added exemplary usage flow.
- Fixed a few typos and added an example how to use the 'parsed' subdictionary in the headers dictionary.

## 1.7 (11 December 2023)
### Features
(no changes)

### Fixes
- Fixed a bug where the JWT payload whose length was not a multiple of 4 could not be decoded by pyCZDS and thus led to a problem when authenticating with the CZDS web service (thanks to [Marcin Szopa for reporting this issue and Tiago Martins for submitting a pull request](https://github.com/mdiez/pyCZDS/issues/2)!).

### Tests
(no changes)

### Internals
(no changes)

### Documentation
(no changes)

## 1.6 (08 May 2023)
### Features
(no changes)

### Fixes
- Fixed a bug where a JWT payload whose length was not a multiple of 4 could not be decoded by pyCZDS (thanks to [Tom Laermans for reporting this issue](https://github.com/mdiez/pyCZDS/issues/1)!).
- Fixed incompatibility of certain Python versions with the importlib.metadata call used to construct the header for requests (the library's version is now hardcoded).

### Tests
(no changes)

### Internals
- Introduced typing for all functions

### Documentation
- Specified that the type returned by the header function is a `requests.models.CaseInsensitiveDict`.