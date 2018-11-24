# evfuncs
Functions for working with files created by EvTAF and the evsonganaly GUI.
In case you need to work with those files in Python 😊😊😊 (see "Usage" below).

The first work published with data collected using EvTAF and evsonganaly is in this paper:  
Tumer, Evren C., and Michael S. Brainard.  
"Performance variability enables adaptive plasticity of ‘crystallized’adult birdsong."
Nature 450.7173 (2007): 1240.  
<https://www.nature.com/articles/nature06390>  

These functions are translations to Python of the original functions 
written in MATLAB (copyright Mathworks) by Evren Tumer.

### Installation
`$ pip install evfuncs`

### Usage

The main purpose for developing these functions in Python was to 
work with files of Bengalese finch song in this data repository:  
<https://figshare.com/articles/Bengalese_Finch_song_repository/4805749>

Using them you can load the `.cbin` audio files ...
```Python
>>> import evfuncs

>>> rawsong, samp_freq = evfuncs.load_cbin('gy6or6_baseline_230312_0808.138.cbin')
```

... and the annotation in the .not.mat files ...
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.cbin')
```
(or, using the .not.mat filename directly)
```Python
>>> notmat_dict = evfuncs.load_notmat('gy6or6_baseline_230312_0808.138.not.mat')
```

...and you should be able to reproduce the segmentation of the raw audio
into syllables and silent periods
```Python

>>> smooth = evfuncs.smooth_data(rawsong, samp_freq)
>>> min_int = notmat_dict['min_int']
>>> min_dur = notmat_dict['min_dur']
>>> threshold = notmat_dict['threshold']
>>> onsets, offsets = evfuncs.segment_song(smooth, min_int, min_dur, threshold)
>>> import numpy as np
>>> np.allclose(onsets, notmat_dict['onsets'])
True
```

The `evfuncs` functions are used in the 
['hybrid-vocal-classifier']() 
and ['songdeck']() libraries.

### Getting Help
Please feel free to raise an issue here:  
https://github.com/NickleDave/evfuncs/issues

### License
[BSD License](./LICENSE).

[![Build Status](https://travis-ci.com/NickleDave/evfuncs.svg?branch=master)](https://travis-ci.com/NickleDave/evfuncs)