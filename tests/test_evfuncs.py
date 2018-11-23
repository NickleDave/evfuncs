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
            self.assertTrue(type(fs) == int or type(fs) == float)

    def test_load_notmat(self):
        self.assertTrue(False)

    def test_bandpass_filtfilt(self):
        self.assertTrue(False)

    def test_smooth_data(self):
        self.assertTrue(False)