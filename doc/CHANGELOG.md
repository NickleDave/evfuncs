# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.1
### Fixed
- fix development status within classifiers option of pyproject.toml
  [e7eee87](https://github.com/NickleDave/evfuncs/commit/e7eee870e3f1dc519acf5e6bd658b3c802a05841)

## 0.3.0
### Changed
- make it so that functions accept filenames as either string or `pathlib.Path`s
  [bd3494c](https://github.com/NickleDave/evfuncs/commit/bd3494c58bb32ce37b3cecc90d87469c075dca37)
- switch to using `poetry` for development
  [376e321](https://github.com/NickleDave/evfuncs/commit/376e3211ae6dc3e6a260c4da7967207f705634de)

## 0.2.1
### Fixed
- change `__init__.py` to import metadata from `__about__.py`, so that version 
is actually single-sourced (both __init__ and setup get it from same place)

## 0.2.0
### Added
- `__about__.py` file, to single-source version info and other metadata

### Changed
- `setup.py` uses `__about__.py` for version + other metadata

## Removed
- an extra `__init__.py` file that was in `src/`

## 0.1.1
- First real production version (now that I kind of mostly understand semantic versioning)
### Added
- Examples sections to most function docstrhttps://github.com/NickleDave/evfuncs/commit/bd3494c58bb32ce37b3cecc90d87469c075dca37ings

### Changed
- setup.py requires scipy>=1.2.0, fixes FutureWarnings raised by scipy.signal 
  (used in `evfuncs.bandpass_filtfilt`)

## 0.1.1a3
### Added
- actually add a changelog
- make a DOI
- add an image of Evren, because this is important

## 0.1.1a2
### Added
- Add evfuncs.segment_notes function and tests for it
- Add Matlab script `make_oracle_data_for_tests.m` that generates "oracle" data from 
actual functions written by Evren and saves in .mat files for comparison with output
from evfuncs

## 0.1.1a1
- Initial version after excising from hvc (https://github.com/NickleDave/hybrid-vocal-classifier/commits/0c50144d75e3a3205db82add8b48302edbbed511/hvc/evfuncs.py)
### Changed
- Change `evfuncs.readrecf` to consistently parse values the same way, e.g. sampling frequency always returned as an int
- Convert tests to Python unittest format (instead of using PyTest library)
- Change defaults for `evfuncs.smooth_data` so it acts like `SmoothData.m` (and passes those defaults to `evfuncs.bandpass_filtfilt`)
### Added
- Write README.md with usage
