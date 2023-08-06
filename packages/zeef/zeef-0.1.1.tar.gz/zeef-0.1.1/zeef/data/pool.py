"""
    Data pool for pool-based query strategies.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 10/12/2021
"""

import numpy as np
from .base import DataHost


class Pool(DataHost):
    """
    Data Pool for pool-based query strategies.
    """

    def __init__(self, raw_data):
        self.data = raw_data
        self.size = len(self.data)
        self.labels = np.empty(len(self.data))
        self.labeled_ids = set()

    def get_unlabeled_data(self):
        """
        Get the unlabeled data.
        :return: numpy array of unlabeled data objects.
        """
        return np.delete(self.data, list(self.labeled_ids), 0)

    def get_unlabeled_ids(self):
        """
        Get the unlabeled data ids, used for query in the unlabeled data pool.
        :return: a list (numpy array) contains all the unlabeled data ids.
        """
        return np.delete(range(self.size), list(self.labeled_ids))

    def label_by_ids(self, label_index_list, labels):
        """
        Label the data by given data ids, those ids should be existed in the given total
        data pool. The labels is a list of labels for corresponding indexed data points.

        :param label_index_list: a list of data ids.
        :param labels: a list of labels.
        :return: None
        """
        if len(label_index_list) == len(labels):
            self.labeled_ids.update(label_index_list)
            self.labels[label_index_list] = labels
        else:
            raise ValueError("the labeled data number should be the same as the corresponding labels.")

    def label_by_id(self, label_index, y):
        """
        Label single data point by indexing the data location.

        :param label_index: the index of the data point you want to label.
        :param y: the data label.
        :return: None
        """
        if label_index < self.size:
            self.labels[label_index] = y
            self.labeled_ids.update([label_index])
        else:
            raise ValueError("make sure the given index is available")

    def label(self, x, y):
        """
        Label the single data by querying the data object itself.

        :param x: The data object you want to label.
        :param y: the data label.
        :return: None
        """
        if x in self.data:
            self.labels[np.where(self.data == x)] = y
        else:
            self.data = np.append(self.data, x)
            self.labels = np.append(self.labels, y)
            self.size += + 1
        self.labeled_ids.update(np.where(self.data == x)[0].tolist())

    def get_labeled_data(self):
        """
        Get all the labeled data objects, including the data and corresponding labels.
        :return: data, labels.
        """
        filter_ids = list(self.labeled_ids)
        return self.data[filter_ids], self.labels[filter_ids]
