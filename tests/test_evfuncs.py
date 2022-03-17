"""
test evfuncs module
"""
import numpy as np
from scipy.io import loadmat

import evfuncs


def test_readrecf(rec_files):
    for rec_file in rec_files:
        rec_dict = evfuncs.readrecf(rec_file)
        assert 'header' in rec_dict
        assert type(rec_dict['header']) == list
        assert 'sample_freq' in rec_dict
        assert type(rec_dict['sample_freq']) == int or type(rec_dict['sample_freq']) == float
        assert 'num_channels' in rec_dict
        assert type(rec_dict['num_channels']) == int
        assert 'num_samples' in rec_dict
        assert type(rec_dict['num_samples']) == int
        assert 'iscatch' in rec_dict
        assert 'outfile' in rec_dict
        assert 'time_before' in rec_dict
        assert type(rec_dict['time_before']) == float
        assert 'time_after' in rec_dict
        assert type(rec_dict['time_after']) == float
        assert 'thresholds' in rec_dict
        assert type(rec_dict['thresholds']) == list
        assert all(
            [type(thresh) == float for thresh in rec_dict['thresholds']]
        )
        assert 'feedback_info' in rec_dict
        assert type(rec_dict['feedback_info']) == dict


def test_load_cbin(cbins):
    for cbin in cbins:
        dat, fs = evfuncs.load_cbin(cbin)
        assert type(dat) == np.ndarray
        assert dat.dtype == '>i2'  # should be big-endian 16 bit
        assert type(fs) == int


def test_load_notmat(notmats):
    for notmat in notmats:
        notmat_dict = evfuncs.load_notmat(notmat)
        assert type(notmat_dict) is dict
        assert 'onsets' in notmat_dict
        assert type(notmat_dict['onsets']) == np.ndarray
        assert notmat_dict['onsets'].dtype == float
        assert 'offsets' in notmat_dict
        assert type(notmat_dict['offsets']) == np.ndarray
        assert notmat_dict['offsets'].dtype == float
        assert 'labels' in notmat_dict
        assert type(notmat_dict['labels']) == str
        assert 'Fs' in notmat_dict
        assert type(notmat_dict['Fs']) == int
        assert 'fname' in notmat_dict
        assert type(notmat_dict['fname']) == str
        assert 'min_int' in notmat_dict
        assert type(notmat_dict['min_int']) == int
        assert 'min_dur' in notmat_dict
        assert type(notmat_dict['min_dur']) == int
        assert 'threshold' in notmat_dict
        assert type(notmat_dict['threshold']) == int
        assert 'sm_win' in notmat_dict
        assert type(notmat_dict['sm_win']) == int


def test_load_notmat_single_annotated_segment(notmat_with_single_annotated_segment):
    notmat_dict = evfuncs.load_notmat(notmat_with_single_annotated_segment)
    assert type(notmat_dict) is dict
    assert 'onsets' in notmat_dict
    assert type(notmat_dict['onsets']) == np.ndarray
    assert notmat_dict['onsets'].dtype == float
    assert 'offsets' in notmat_dict
    assert type(notmat_dict['offsets']) == np.ndarray
    assert notmat_dict['offsets'].dtype == float
    assert 'labels' in notmat_dict
    assert type(notmat_dict['labels']) == str
    assert 'Fs' in notmat_dict
    assert type(notmat_dict['Fs']) == int
    assert 'fname' in notmat_dict
    assert type(notmat_dict['fname']) == str
    assert 'min_int' in notmat_dict
    assert type(notmat_dict['min_int']) == int
    assert 'min_dur' in notmat_dict
    assert type(notmat_dict['min_dur']) == int
    assert 'threshold' in notmat_dict
    assert type(notmat_dict['threshold']) == int
    assert 'sm_win' in notmat_dict
    assert type(notmat_dict['sm_win']) == int


def test_bandpass_filtfilt_works(cbins, filtsong_mat_files):
    for cbin, filtsong_mat_file in zip(cbins, filtsong_mat_files):
        dat, fs = evfuncs.load_cbin(cbin)
        filtsong = evfuncs.bandpass_filtfilt(dat, fs)
        assert type(filtsong) == np.ndarray
        filtsong_mat = loadmat(filtsong_mat_file)
        filtsong_mat = np.squeeze(filtsong_mat['filtsong'])
        assert np.allclose(filtsong, filtsong_mat)


def test_smooth_data(cbins, smooth_data_mat_files):
    for cbin, smooth_data_mat_file in zip(cbins, smooth_data_mat_files):
        dat, fs = evfuncs.load_cbin(cbin)
        smoothed = evfuncs.smooth_data(dat, fs, freq_cutoffs=None)
        smoothed_500_10k = evfuncs.smooth_data(dat, fs,
                                               freq_cutoffs=(500, 10000))
        assert type(smoothed) == np.ndarray
        assert type(smoothed_500_10k) == np.ndarray
        assert not np.all(np.equal(smoothed, smoothed_500_10k))
        smooth_data_mat = loadmat(smooth_data_mat_file)
        smooth_data_mat = np.squeeze(smooth_data_mat['sm'])
        assert np.allclose(smoothed_500_10k, smooth_data_mat)


def test_segment_song(cbins, notmats, segment_mats):
    for cbin, notmat, segment_mat in zip(cbins, notmats, segment_mats):
        dat, fs = evfuncs.load_cbin(cbin)
        smooth = evfuncs.smooth_data(dat, fs)
        nmd = evfuncs.load_notmat(notmat)
        min_syl_dur = nmd['min_dur'] / 1000
        min_silent_dur = nmd['min_int'] / 1000
        threshold = nmd['threshold']
        onsets, offsets = evfuncs.segment_song(smooth, fs,
                                               threshold, min_syl_dur, min_silent_dur)
        segment_dict = loadmat(segment_mat, squeeze_me=True)
        onsets_mat = segment_dict['onsets']
        offsets_mat = segment_dict['offsets']
        # set tolerances for numpy.allclose check.
        # difference np.abs(offsets - offsets_mat) is usually ~0.00003125...
        # We just don't want error to be larger than a millisecond
        # By trial and error, I find that these vals for tolerance result in
        # about that ceiling
        atol = 0.0005
        rtol = 0.00001
        # i.e., 0.0005 + 0.00001 * some_onsets_or_offset_array ~ [0.0005, 0.0005, ...]
        assert np.allclose(onsets, onsets_mat, rtol, atol)
        assert np.allclose(offsets, offsets_mat, rtol, atol)
