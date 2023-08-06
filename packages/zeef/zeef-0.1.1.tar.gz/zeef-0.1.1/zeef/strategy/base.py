"""
    Pool-based active learning strategy base class.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 07/12/2021
"""

from zeef.learner.torch_learner import Learner
from ..data import DataHost


class Strategy:
    def __init__(self, data_host: DataHost, learner: Learner):
        self.learner = learner
        self.data_host = data_host

    def query(self, number):
        """
        The query function that calls the specific active learning strategy.
        :param number: the query number.
        :return: the data ids in a numpy array.
        """
        pass

    def query_object(self, number):
        """
        The query function that calls the specific active learning strategy.
        :param number: the query number.
        :return: the data points in a numpy array.
        """
        pass

    def update(self, labeled_ids, labels):
        """
        Update the data pool with labels.
        :param labeled_ids: the ids of labeled data.
        :param labels: the corresponding data labels.
        :return: None
        """
        self.data_host.label(labeled_ids, labels)

    def learn(self, n_epoch=1, batch_size=1, transform=None):
        """
        Train the model using all the labeled data.
        @return: None
        """
        self.learner.learn(*self.data_host.get_labeled_data(), n_epoch, batch_size=batch_size, transform=transform)

    def infer(self, data, batch_size=1, is_prob=False):
        """
        Inference function by given request data.
        @param data: the inference raw data.
        @param batch_size: the inference batch_size.
        @param is_prob: is_prob: the return values or probabilities.
        @return: the inference results.
        """
        return self.learner.infer(data, batch_size=batch_size, is_prob=is_prob)
