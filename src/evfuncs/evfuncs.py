"""
ev_funcs
Python implementations of functions used with EvTAF and evsonganaly.m
"""
from pathlib import Path

import numpy as np
from scipy.io import loadmat
import scipy.signal


def readrecf(filename):
    """reads .rec files output by EvTAF
    and returns rec_dict with (approximately)
    the same structure as the rec struct
    returned by readrec.m

    Parameters
    ----------
    filename : str, Path
        name of .rec file, can include path

    Returns
    -------
    rec_dict : dict
        with following key, value pairs
            header : str
                header from .rec file
            time_before : float
                time in seconds of additional audio added to file by EvTAF
                from before sound amplitude went above threshold for recording
            time_after : float
                time in seconds of additional audio added to file by EvTAF
                after sound amplitude dropped below threshold for recording
            iscatch : bool
                list of whether each occurrence of auditory feedback triggered
                was a 'catch trial' (where feedback would have been triggered but
                was withheld so behavior on that trial could be measured)
            num_channels : int
                number of channels from DAQ board recored by EvTAF
            sample_freq : int
                sampling frequency of audio file associated with this .rec file, in Hertz
            num_samples : int
                number of audio samples in file
            outfile : str
                name of audio file played as auditory feedback (if there was any)
            thresholds : int
                thresholds used by ring counter to determine whether to trigger auditory feedback
            feedback_info : dict
                maps feedback type to time it occurred in milliseconds

    Examples
    --------
    >>> recf = 'gy6or6_baseline_230312_0808.138.rec'
    >>> rec_dict = readrecf(recf)
    >>> num_samples = rec_dict['num_samples'}
    >>> sample_freq = rec_dict['sample_freq'}
    >>> print(f"file duration in seconds: {num_samples / sample_freq:.3f}")
    file duration in seconds: 12.305
    """
    filename = Path(filename)

    rec_dict = {}
    with filename.open('r') as recfile:
        line_tmp = ""
        while 1:
            if line_tmp == "":
                line = recfile.readline()
            else:
                line = line_tmp
                line_tmp = ""
                
            if line == "":  # if End Of File
                break
            elif line == "\n":  # if blank line
                continue
            elif "Catch" in line:
                ind = line.find('=')
                rec_dict['iscatch'] = line[ind+1:]
            elif "Chans" in line:
                ind = line.find('=')
                rec_dict['num_channels'] = int(line[ind+1:])
            elif "ADFREQ" in line:
                ind = line.find('=')
                try:
                    rec_dict['sample_freq'] = int(line[ind+1:])
                except ValueError:
                    # if written with scientific notation
                    # first parse as float, then cast to int
                    sample_freq_float = float(line[ind+1:])
                    try:
                        rec_dict['sample_freq'] = int(sample_freq_float)
                    except ValueError:
                        raise ValueError("Couldn't convert following value for "
                                         "ADFREQ in .rec file {} to an integer: "
                                         "{}".format(filename,
                                                     sample_freq_float))
            elif "Samples" in line:
                ind = line.find('=')
                rec_dict['num_samples'] = int(line[ind+1:])
            elif "T After" in line or "T AFTER" in line:
                ind = line.find('=')
                rec_dict['time_after'] = float(line[ind+1:])
            elif "T Before" in line or "T BEFORE" in line:
                ind = line.find('=')
                rec_dict['time_before'] = float(line[ind+1:])
            elif "Output Sound File" in line:
                ind = line.find('=')
                rec_dict['outfile'] = line[ind+1:]
            elif "Thresholds" in line or "THRESHOLDS" in line:
                th_list = []
                while 1:
                    line = recfile.readline()
                    if line == "":
                        break
                    try:
                        th_list.append(float(line))
                    except ValueError:  # because we reached next section
                        line_tmp = line
                        break
                rec_dict['thresholds'] = th_list
                if line == "":
                    break
            elif "Feedback information" in line:
                fb_dict = {}
                while 1:
                    line = recfile.readline()
                    if line == "":
                        break
                    elif line == "\n":
                        continue
                    ind = line.find("msec")
                    time = float(line[:ind-1])
                    ind = line.find(":")
                    fb_type = line[ind+2:]
                    fb_dict[time] = fb_type
                rec_dict['feedback_info'] = fb_dict
                if line == "":
                    break
            elif "File created" in line:
                header = [line]
                for counter in range(4):
                    line = recfile.readline()
                    header.append(line)
                rec_dict['header']=header
    return rec_dict


def load_cbin(filename, channel=0):
    """loads .cbin files output by EvTAF.
    
    Parameters
    ----------
    filename : str
        name of .cbin file, can include path
    channel : int
        Channel in file to load. Default is 0.

    Returns
    -------
    data : numpy.ndarray
        1-d vector of 16-bit signed integers
    sample_freq : int or float
        sampling frequency in Hz. Typically 32000.

    Examples
    --------
    >>> cbin_filename = 'gy6or6_baseline_230312_0808.138.cbin'
    >>> data, sample_freq = load_cbin(cbin_filename)
    >>> data
    array([-230, -223, -235, ...,   34,   36,   26], dtype=int16)
    """
    filename = Path(filename)

    # .cbin files are big endian, 16 bit signed int, hence dtype=">i2" below
    data = np.fromfile(filename, dtype=">i2")
    recfile = filename.parent.joinpath(filename.stem + '.rec')
    rec_dict = readrecf(recfile)
    data = data[channel::rec_dict['num_channels']]  # step by number of channels
    sample_freq = rec_dict['sample_freq']
    return data, sample_freq


def load_notmat(filename):
    """loads .not.mat files created by evsonganaly (Matlab GUI for labeling song)

    Parameters
    ----------
    filename : str
        name of .not.mat file, can include path

    Returns
    -------
    notmat_dict : dict
        variables from .not.mat files

    Examples
    --------
    >>> a_notmat = 'gy6or6_baseline_230312_0808.138.cbin.not.mat'
    >>> notmat_dict = load_notmat(a_notmat)
    >>> notmat_dict.keys()
    dict_keys(['__header__', '__version__', '__globals__', 'Fs', 'fname', 'labels',
    'onsets', 'offsets', 'min_int', 'min_dur', 'threshold', 'sm_win'])

    Notes
    -----
    Basically a wrapper around `scipy.io.loadmat`. Calls `loadmat` with `squeeze_me=True`
    to remove extra dimensions from arrays that `loadmat` parser sometimes adds.

    Also note that **onsets and offsets from .not.mat files are in milliseconds**.
    The GUI `evsonganaly` saves onsets and offsets in these units,
    and we avoid converting them here for consistency and interoperability
    with Matlab code.
    """
    filename = Path(filename)

    # have to cast to str and call endswith because 'ext' from Path will just be .mat
    if str(filename).endswith(".not.mat"):
        pass
    elif str(filename).endswith("cbin"):
        filename = filename.parent.joinpath(filename.name + ".not.mat")
    else:
        raise ValueError(
            f"Filename should have extension .cbin.not.mat or .cbin but extension was: {ext}"
        )
    return loadmat(filename, squeeze_me=True)


def bandpass_filtfilt(rawsong, samp_freq, freq_cutoffs=(500, 10000)):
    """filter song audio with band pass filter, then perform zero-phase
    filtering with filtfilt function

    Parameters
    ----------
    rawsong : ndarray
        audio
    samp_freq : int
        sampling frequency
    freq_cutoffs : list
        2 elements long, cutoff frequencies for bandpass filter.
        Default is [500, 10000].

    Returns
    -------
    filtsong : ndarray
    """
    if freq_cutoffs[0] <= 0:
        raise ValueError('Low frequency cutoff {} is invalid, '
                         'must be greater than zero.'
                         .format(freq_cutoffs[0]))

    Nyquist_rate = samp_freq / 2
    if freq_cutoffs[1] >= Nyquist_rate:
        raise ValueError('High frequency cutoff {} is invalid, '
                         'must be less than Nyquist rate, {}.'
                         .format(freq_cutoffs[1], Nyquist_rate))

    if rawsong.shape[-1] < 387:
        numtaps = 64
    elif rawsong.shape[-1] < 771:
        numtaps = 128
    elif rawsong.shape[-1] < 1539:
        numtaps = 256
    else:
        numtaps = 512

    cutoffs = np.asarray([freq_cutoffs[0] / Nyquist_rate,
                          freq_cutoffs[1] / Nyquist_rate])
    # code on which this is based, bandpass_filtfilt.m, says it uses Hann(ing)
    # window to design filter, but default for matlab's fir1
    # is actually Hamming
    # note that first parameter for scipy.signal.firwin is filter *length*
    # whereas argument to matlab's fir1 is filter *order*
    # for linear FIR, filter length is filter order + 1
    b = scipy.signal.firwin(numtaps + 1, cutoffs, pass_zero=False)
    a = np.zeros((numtaps+1,))
    a[0] = 1  # make an "all-zero filter"
    padlen = np.max((b.shape[-1] - 1, a.shape[-1] - 1))
    filtsong = scipy.signal.filtfilt(b, a, rawsong, padlen=padlen)
    return filtsong


def smooth_data(rawsong, samp_freq, freq_cutoffs=(500, 10000), smooth_win=2):
    """filter raw audio and smooth signal
    used to calculate amplitude.

    Parameters
    ----------
    rawsong : ndarray
        1-d numpy array, "raw" voltage waveform from microphone
    samp_freq : int
        sampling frequency
    freq_cutoffs: list
        two-element list of integers, [low freq., high freq.]
        bandpass filter applied with this list defining pass band.
        If None, in which case bandpass filter is not applied.
    smooth_win : integer
        size of smoothing window in milliseconds. Default is 2.

    Returns
    -------
    smooth : ndarray
        1-d numpy array, smoothed waveform

    Applies a bandpass filter with the frequency cutoffs in spect_params,
    then rectifies the signal by squaring, and lastly smooths by taking
    the average within a window of size sm_win.
    This is a very literal translation from the Matlab function SmoothData.m
    by Evren Tumer. Uses the Thomas-Santana algorithm.
    """
    if freq_cutoffs is None:
        # then don't do bandpass_filtfilt
        filtsong = rawsong
    else:
        filtsong = bandpass_filtfilt(rawsong, samp_freq, freq_cutoffs)

    squared_song = np.power(filtsong, 2)
    len = np.round(samp_freq * smooth_win / 1000).astype(int)
    h = np.ones((len,)) / len
    smooth = np.convolve(squared_song, h)
    offset = round((smooth.shape[-1] - filtsong.shape[-1]) / 2)
    smooth = smooth[offset:filtsong.shape[-1] + offset]
    return smooth


def segment_song(smooth, samp_freq, threshold=5000, min_syl_dur=0.02,
                 min_silent_dur=0.002, return_Hz=False):
    """segment audio file of birdsong into syllables

    Parameters
    ----------
    smooth : np.ndarray
        Smoothed audio waveform, returned by evfuncs.smooth_data
    samp_freq : int
        Sampling frequency at which audio was recorded. Returned by
        evfuncs.load_cbin.
    threshold : int
        value above which amplitude is considered part of a segment.
        Default is 5000.
    min_syl_dur : float
        minimum duration of a segment.
        In .not.mat files saved by evsonganaly, this value is called "min_dur"
        Default is 0.02, i.e. 20 ms.
    min_silent_dur : float
        minimum duration of silent gap between segment.
        In .not.mat files saved by evsonganaly, this value is called "min_int"
        Default is 0.002, i.e. 2 ms.
    return_Hz : bool
        if True, returns the onsets and offsets in units of Hz.
        Default is False.

    Returns
    -------
    onsets_s : np.ndarray
        Onset times of syllables in song, in seconds.
    offsets_s : np.ndarray
        Offset times of syllables in song, in seconds.
    onsets_Hz : np.ndarray
        Onset times of syllables in song, in seconds.
        Only returned if "return_Hz" is True.
    offsets_Hz : np.ndarray
        Offset times of syllables in song, in seconds.
        Only returned if "return_Hz" is True.

    Equivalent to SegmentNotes.m function that is part of evsonganaly GUI.
    """
    above_th = smooth > threshold
    h = [1, -1]
    # convolving with h causes:
    # +1 whenever above_th changes from 0 to 1
    # and -1 whenever above_th changes from 1 to 0
    above_th_convoluted = np.convolve(h, above_th)

    # always get in units of Hz first, then convert to s
    onsets_Hz = np.where(above_th_convoluted > 0)[0]
    offsets_Hz = np.where(above_th_convoluted < 0)[0]
    onsets_s = onsets_Hz / samp_freq
    offsets_s = offsets_Hz / samp_freq

    if onsets_s.shape[0] < 1 or offsets_s.shape[0] < 1:
        return None, None  # because no onsets or offsets in this file

    # get rid of silent intervals that are shorter than min_silent_dur
    silent_gap_durs = onsets_s[1:] - offsets_s[:-1]  # duration of silent gaps
    keep_these = np.nonzero(silent_gap_durs > min_silent_dur)
    onsets_s = np.concatenate(
        (onsets_s[0, np.newaxis], onsets_s[1:][keep_these]))
    offsets_s = np.concatenate(
        (offsets_s[:-1][keep_these], offsets_s[-1, np.newaxis]))
    if return_Hz:
        onsets_Hz = np.concatenate(
            (onsets_Hz[0, np.newaxis], onsets_Hz[1:][keep_these]))
        offsets_Hz = np.concatenate(
            (offsets_Hz[:-1][keep_these], offsets_Hz[-1, np.newaxis]))

    # eliminate syllables with duration shorter than min_syl_dur
    syl_durs = offsets_s - onsets_s
    keep_these = np.nonzero(syl_durs > min_syl_dur)
    onsets_s = onsets_s[keep_these]
    offsets_s = offsets_s[keep_these]
    if return_Hz:
        onsets_Hz = onsets_Hz[keep_these]
        offsets_Hz = offsets_Hz[keep_these]

    if return_Hz:
        return onsets_s, offsets_s, onsets_Hz, offsets_Hz
    else:
        return onsets_s, offsets_s
