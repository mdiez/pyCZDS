# pyCZDS Changelog

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