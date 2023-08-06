"""
    Basic SKLearn learner class for different platform.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 15/12/2021
"""
import numpy as np
from tqdm import tqdm
from .base import Learner


class SKLearner(Learner):
    def __init__(self, net):
        self.net = net

    def learn(self, data_x, data_y, n_epoch=1, batch_size=1, transform=None):
        # TODO: needs test
        if hasattr(self.net, 'batch_size'):
            self.net.batch_size = batch_size

        for _ in tqdm(range(n_epoch)):
            self.net.fit(data_x, data_y)

    def infer(self, data, batch_size=1, is_prob=False):
        outputs = []
        batches = np.split(data, batch_size)
        for batch in batches:
            if is_prob:
                outputs.append(self.net.predict_proba(batch))
            else:
                outputs.append(self.net.predict(batch))
        return np.concatenate(outputs)
