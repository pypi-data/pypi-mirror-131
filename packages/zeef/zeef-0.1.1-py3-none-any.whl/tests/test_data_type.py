"""
    Unit tests for different I/O data modalities.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 06/12/2021
"""

import unittest

import numpy as np
from numpy import random

from zeef.data import Pool
from zeef.strategy import RandomSampling


class TestDataType(unittest.TestCase):

    def test_random_pick(self):
        raw_data = np.ones(100)
        pool = Pool(raw_data)
        pool.label_by_ids(range(50, 60, 1), np.zeros(10))
        x, y = pool.get_labeled_data()
        self.assertEqual(x.tolist(), np.ones(10).tolist())
        self.assertEqual(y.tolist(), np.zeros(10).tolist())


if __name__ == '__main__':
    unittest.main()
