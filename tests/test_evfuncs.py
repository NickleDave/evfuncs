"""
test evfuncs module
"""
import os
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
        rec = os.path.join(self.test_data_dir,
                           'gy6or6_baseline_230312_0808.138.rec')
        rec_dict = evfuncs.readrecf(rec)
        self.assertTrue('header' in rec_dict)
        self.assertTrue(type(rec_dict['header']) == list)
        self.assertTrue('sample_freq' in rec_dict)
        self.assertTrue(type(rec_dict['sample_freq']) == int)
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
            [type(thresh)==float for thresh in rec_dict['thresholds']]
        ))
        self.assertTrue('feedback_info' in rec_dict)
        self.assertTrue(type(rec_dict['feedback_info']) == dict)

    def test_load_cbin(self):
        cbin = os.path.join(self.test_data_dir,
                            'gy6or6_baseline_230312_0808.138.cbin')
        dat, fs = evfuncs.load_cbin(cbin)
        self.assertTrue(type(dat) == np.ndarray)
        self.assertTrue(dat.dtype == '>i2')  # should be big-endian 16 bit
        self.assertTrue(type(fs) == int)
