# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.5] -- 2022-05-14
### Changed
- raise minimum required Python to 3.8, 
  to adhere to [NEP-29](https://numpy.org/neps/nep-0029-deprecation_policy.html)
  [#18](https://github.com/NickleDave/evfuncs/pull/18).
  Fixes [#17](https://github.com/NickleDave/evfuncs/issues/17).

## [0.3.4] -- 2022-03-17
### Changed
- change `evfuncs.load_notmat` so that the returned values for 
  `onsets` and `offsets` will always be `numpy.ndarray`, even when 
  the `.not.mat` only has a single annotated segment.
  [#16](https://github.com/NickleDave/evfuncs/pull/16)
  Fixes [#14](https://github.com/NickleDave/evfuncs/issues/14)

## [0.3.3] -- 2021-12-30
### Added
- added `CITATION.cff` file
  [#11](https://github.com/NickleDave/evfuncs/pull/11)

### Changed
- switch to using `flit` for development, to have PEP 621 metadata 
  and to not need `poetry` for `conda-forge` recipe, 
  that imposes limits on Python version
  [#12](https://github.com/NickleDave/evfuncs/pull/12)
- require minimum version of Python to be 3.7 
  [#13](https://github.com/NickleDave/evfuncs/pull/13)

## 0.3.2.post1 -- 2021-03-04
### Changed
- add metadata to pyproject.toml so that README is used as "long description" 
  and appears on PyPI
  [43c0742](https://github.com/NickleDave/evfuncs/commit/43c07428b8237b81bd0b80c61b5b27950ebb11bc)

## 0.3.2 -- 2021-03-04
### Changed
- switch to using GitHub Actions for continuous integration
  [62c1b89](https://github.com/NickleDave/evfuncs/commit/62c1b89a5bbcf12ac8c6929c79e46a9e966d7d47)

### Fixed
- change dependencies and required Python so they are not pinned to major version
  [65480ac](https://github.com/NickleDave/evfuncs/commit/65480ac3c50df6533284f57933134d9e34277086)

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
