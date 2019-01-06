# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## 0.1.1
- First real production version (now that I kind of mostly understand semantic versioning)
### Added
- Examples sections to most function docstrings

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
