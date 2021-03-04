[![Build Status](https://github.com/NickleDave/evfuncs/actions/workflows/ci.yml/badge.svg)
[![DOI](https://zenodo.org/badge/158776329.svg)](https://zenodo.org/badge/latestdoi/158776329)
[![PyPI version](https://badge.fury.io/py/evfuncs.svg)](https://badge.fury.io/py/evfuncs)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
# *ev*funcs
Functions for working with files created by EvTAF and the evsonganaly GUI.  
In case you need to work with those files in Python 😊😊😊 (see "Usage" below).

The first work published with data collected using EvTAF and evsonganaly is in this paper:  
Tumer, Evren C., and Michael S. Brainard.  
"Performance variability enables adaptive plasticity of ‘crystallized’adult birdsong."  
Nature 450.7173 (2007): 1240.  
<https://www.nature.com/articles/nature06390>  

These functions are translations to Python of the original functions 
written in MATLAB (copyright Mathworks) by Evren Tumer (shown below).  
<p style="text-align:center;">
<img src="./doc/ev_ev_ev.png" alt="Image of Evren">
</p>

### Installation
`$ pip install evfuncs`

### Usage

The main purpose for developing these functions in Python was to 
work with files of Bengalese finch song in this data repository: 
<https://figshare.com/articles/Bengalese_Finch_song_repository/4805749>

Using `evfuncs` with that repository, you can load the `.cbin` audio files ...
```Python
>>> import evfuncs

>>> rawsong, samp_freq = evfuncs.load_cbin('gy6or6_baseline_230312_0808.138.cbin')
```

... and the annotation in the `.not.mat` files ...
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.cbin')
```
(or, using the `.not.mat` filename directly)
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.not.mat')
```

...and you should be able to reproduce the segmentation of the raw audio files of birdsong
into syllables and silent periods, using the segmenting parameters from a .not.mat file and 
the simple algorithm applied by the SegmentNotes.m function.

```Python
>>> smooth = evfuncs.smooth_data(rawsong, samp_freq)
>>> threshold = notmat_dict['threshold']
>>> min_syl_dur = notmat_dict['min_dur'] / 1000
>>> min_silent_dur = notmat_dict['min_int'] / 1000
>>> onsets, offsets = evfuncs.segment_song(smooth, samp_freq, threshold, min_syl_dur, min_silent_dur)
>>> import numpy as np
>>> np.allclose(onsets, notmat_dict['onsets'])
True
```
(*Note that this test would return `False` if the onsets and offsets in the .not.mat 
annotation file had been modified, e.g., a user of the evsonganaly GUI had edited them,
after they were originally computed by the SegmentNotes.m function.*)

`evfuncs` is used to load annotations by  
['crowsetta'](https://github.com/NickleDave/crowsetta), 
a data-munging tool for building datasets of vocalizations 
that can be used to train machine learning models.
Two machine learning libraries that can use those datasets are: 
[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/), 
and [`vak`](https://github.com/NickleDave/vak).

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/evfuncs/issues

### License
[BSD License](./LICENSE).

### Citation
If you use this package, please cite the DOI:  
[![DOI](https://zenodo.org/badge/158776329.svg)](https://zenodo.org/badge/latestdoi/158776329)

### Build Status
[![Build Status](https://travis-ci.com/NickleDave/evfuncs.svg?branch=master)](https://travis-ci.com/NickleDave/evfuncs)
