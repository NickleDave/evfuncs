"""
test evfuncs module
"""
import os
from glob import glob
import unittest

import numpy as np
from scipy.io import loadmat

import evfuncs


class TestEvfuncs(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.', 'test_data',
            'gy6or6_032312_subset',
        )

    def test_readrecf(self):
        rec_files = sorted(glob(os.path.join(self.test_data_dir, '*.rec')))
        for rec_file in rec_files:
            rec_dict = evfuncs.readrecf(rec_file)
            self.assertTrue('header' in rec_dict)
            self.assertTrue(type(rec_dict['header']) == list)
            self.assertTrue('sample_freq' in rec_dict)
            self.assertTrue(type(rec_dict['sample_freq']) == int
                            or type(rec_dict['sample_freq']) == float)
            self.assertTrue('num_channels' in rec_dict)
            self.assertTrue(type(rec_dict['num_channels']) == int)
            self.assertTrue('num_samples' in rec_dict)
            self.assertTrue(type(rec_dict['num_samples']) == int)
            self.assertTrue('iscatch' in rec_dict)
            self.assertTrue('outfile' in rec_dict)
            self.assertTrue('time_before' in rec_dict)
            self.assertTrue(type(rec_dict['time_before']) == float)
            self.assertTrue('time_after' in rec_dict)
            self.assertTrue(type(rec_dict['time_after']) == float)
            self.assertTrue('thresholds' in rec_dict)
            self.assertTrue(type(rec_dict['thresholds']) == list)
            self.assertTrue(all(
                [type(thresh) == float for thresh in rec_dict['thresholds']]
            ))
            self.assertTrue('feedback_info' in rec_dict)
            self.assertTrue(type(rec_dict['feedback_info']) == dict)

    def test_load_cbin(self):
        cbins = sorted(glob(os.path.join(self.test_data_dir, '*.cbin')))
        for cbin in cbins:
            dat, fs = evfuncs.load_cbin(cbin)
            self.assertTrue(type(dat) == np.ndarray)
            self.assertTrue(dat.dtype == '>i2')  # should be big-endian 16 bit
            self.assertTrue(type(fs) == int)

    def test_load_notmat(self):
        notmats = sorted(glob(os.path.join(self.test_data_dir, '*.not.mat')))
        for notmat in notmats:
            notmat_dict = evfuncs.load_notmat(notmat)
            self.assertTrue(type(notmat_dict) is dict)
            self.assertTrue('onsets' in notmat_dict)
            self.assertTrue(type(notmat_dict['onsets']) == np.ndarray)
            self.assertTrue(notmat_dict['onsets'].dtype == float)
            self.assertTrue('offsets' in notmat_dict)
            self.assertTrue(type(notmat_dict['offsets']) == np.ndarray)
            self.assertTrue(notmat_dict['offsets'].dtype == float)
            self.assertTrue('labels' in notmat_dict)
            self.assertTrue(type(notmat_dict['labels']) == str)
            self.assertTrue('Fs' in notmat_dict)
            self.assertTrue(type(notmat_dict['Fs']) == int)
            self.assertTrue('fname' in notmat_dict)
            self.assertTrue(type(notmat_dict['fname']) == str)
            self.assertTrue('min_int' in notmat_dict)
            self.assertTrue(type(notmat_dict['min_int']) == int)
            self.assertTrue('min_dur' in notmat_dict)
            self.assertTrue(type(notmat_dict['min_dur']) == int)
            self.assertTrue('threshold' in notmat_dict)
            self.assertTrue(type(notmat_dict['threshold']) == int)
            self.assertTrue('sm_win' in notmat_dict)
            self.assertTrue(type(notmat_dict['sm_win']) == int)

    def test_bandpass_filtfilt_works(self):
        cbins = sorted(glob(os.path.join(self.test_data_dir,
                                         '*.cbin')))
        filtsong_mat_files = sorted(glob(os.path.join(self.test_data_dir,
                                                      '*filtsong*.mat')))
        for cbin, filtsong_mat_file in zip(cbins, filtsong_mat_files):
            dat, fs = evfuncs.load_cbin(cbin)
            filtsong = evfuncs.bandpass_filtfilt(dat, fs)
            self.assertTrue(type(filtsong) == np.ndarray)
            filtsong_mat = loadmat(filtsong_mat_file)
            filtsong_mat = np.squeeze(filtsong_mat['filtsong'])
            self.assertTrue(np.allclose(filtsong,
                                        filtsong_mat))

    def test_smooth_data(self):
        cbins = sorted(glob(os.path.join(self.test_data_dir, '*.cbin')))
        smooth_data_mat_files = sorted(glob(os.path.join(self.test_data_dir,
                                                         '*smooth_data*.mat')))
        for cbin, smooth_data_mat_file in zip(cbins, smooth_data_mat_files):
            dat, fs = evfuncs.load_cbin(cbin)
            smoothed = evfuncs.smooth_data(dat, fs, freq_cutoffs=None)
            smoothed_500_10k = evfuncs.smooth_data(dat, fs,
                                                   freq_cutoffs=(500, 10000))
            self.assertTrue(type(smoothed) == np.ndarray)
            self.assertTrue(type(smoothed_500_10k) == np.ndarray)
            self.assertTrue(not np.all(np.equal(smoothed, smoothed_500_10k)))
            smooth_data_mat = loadmat(smooth_data_mat_file)
            smooth_data_mat = np.squeeze(smooth_data_mat['sm'])
            self.assertTrue(np.allclose(smoothed_500_10k,
                                        smooth_data_mat))

    def test_segment_song(self):
        cbins = sorted(glob(os.path.join(self.test_data_dir, '*.cbin')))
        notmats = sorted(glob(os.path.join(self.test_data_dir, '*.not.mat')))
        segment_mats = sorted(glob(os.path.join(self.test_data_dir,
                                                '*unedited_SegmentNotes_output.mat')))
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
            self.assertTrue(np.allclose(onsets, onsets_mat, rtol, atol))
            self.assertTrue(np.allclose(offsets, offsets_mat, rtol, atol))


if __name__ == '__main__':
    unittest.main()
