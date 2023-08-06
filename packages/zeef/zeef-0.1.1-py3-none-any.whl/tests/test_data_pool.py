"""
    Unit tests for Pool-based data selection functions.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 06/12/2021
"""

import unittest

import numpy as np
from numpy import random

from zeef.data import Pool


class TestDataPool(unittest.TestCase):

    def test_label_simple(self):
        raw_data = np.ones(100)
        pool = Pool(raw_data)
        pool.label_by_ids(range(50, 60, 1), np.zeros(10))
        x, y = pool.get_labeled_data()
        self.assertEqual(x.tolist(), np.ones(10).tolist())
        self.assertEqual(y.tolist(), np.zeros(10).tolist())

    def test_label_random(self):
        label_num = 30
        raw_data = random.rand(100)
        x_data = raw_data[:label_num]
        pool = Pool(raw_data)
        pool.label_by_ids(range(0, label_num, 1), np.ones(label_num))
        x, y = pool.get_labeled_data()

        self.assertEqual(x.tolist(), x_data.tolist())
        self.assertEqual(y.tolist(), np.ones(label_num).tolist())

    def test_label_one(self):
        label_num = 30
        raw_data = random.rand(100)
        pool = Pool(raw_data)
        pool.label_by_ids(range(0, label_num, 1), np.ones(label_num))
        pool.label(120, 0)
        x, y = pool.get_labeled_data()
        self.assertEqual(x.tolist()[-1], 120)
        self.assertEqual(y.tolist()[-1], 0)
        self.assertEqual(y.tolist()[0], 1)
        self.assertEqual(pool.size, len(raw_data) + 1)
        self.assertEqual(len(pool.labeled_ids), label_num + 1)
        pool.label_by_id(0, 0)
        pool.label_by_id(10, 2)
        x, y = pool.get_labeled_data()
        self.assertEqual(y.tolist()[0], 0)
        self.assertEqual(y.tolist()[10], 2)
        self.assertEqual(pool.size, len(raw_data) + 1)
        self.assertEqual(len(pool.labeled_ids), label_num + 1)

    def test_get_unlabeled_ids(self):
        label_num = 500
        raw_data = random.rand(1000)
        pool = Pool(raw_data)
        pool.label_by_ids(range(0, label_num, 1), np.ones(label_num))
        unlabeled_ids = list(pool.get_unlabeled_ids())

        self.assertEqual(len(unlabeled_ids), 500)
        self.assertEqual(len(pool.labeled_ids), 500)
        pool.label_by_ids(range(label_num, label_num + 200, 1), np.ones(200))
        unlabeled_ids = list(pool.get_unlabeled_ids())
        self.assertEqual(len(unlabeled_ids), 300)
        self.assertEqual(len(pool.labeled_ids), 700)


if __name__ == '__main__':
    unittest.main()
