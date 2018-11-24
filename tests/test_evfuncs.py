"""
test evfuncs module
"""
import os
from glob import glob
import unittest

import numpy as np

import evfuncs


class TestEvfuncs(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.', 'test_data',
            'gy6or6_032312_subset',
        )

    def test_readrecf(self):
        rec_files = glob(os.path.join(self.test_data_dir, '*.rec'))
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
        cbins = glob(os.path.join(self.test_data_dir, '*.cbin'))
        for cbin in cbins:
            dat, fs = evfuncs.load_cbin(cbin)
            self.assertTrue(type(dat) == np.ndarray)
            self.assertTrue(dat.dtype == '>i2')  # should be big-endian 16 bit
            self.assertTrue(type(fs) == int)

    def test_load_notmat(self):
        notmats = glob(os.path.join(self.test_data_dir, '*.not.mat'))
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

    def test_bandpass_filtfilt(self):
        cbins = glob(os.path.join(self.test_data_dir, '*.cbin'))
        for cbin in cbins:
            dat, fs = evfuncs.load_cbin(cbin)
            filtsong = evfuncs.bandpass_filtfilt(dat, fs)
            self.assertTrue(type(filtsong) == np.ndarray)

    def test_smooth_data(self):
        cbins = glob(os.path.join(self.test_data_dir, '*.cbin'))
        for cbin in cbins:
            dat, fs = evfuncs.load_cbin(cbin)
            smoothed = evfuncs.smooth_data(dat, fs, freq_cutoffs=None)
            smoothed_500_10k = evfuncs.smooth_data(dat, fs,
                                                   freq_cutoffs=(500, 10000))
            self.assertTrue(type(smoothed) == np.ndarray)
            self.assertTrue(type(smoothed_500_10k) == np.ndarray)
            self.assertTrue(not np.all(np.equal(smoothed, smoothed_500_10k)))
