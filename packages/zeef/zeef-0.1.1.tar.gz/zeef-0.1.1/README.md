# Zeef: Active Learning for Data-Centric AI

![PyPI](https://img.shields.io/pypi/v/zeef?color=blue) ![PyPI - Downloads](https://img.shields.io/pypi/dm/zeef) [![Testing](https://github.com/MLSysOps/zeef/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/MLSysOps/zeef/actions/workflows/main.yml) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal?ref=badge_shield)

An active learning framework that can be applied to real-world scenarios that leak labeled data.

## Installation

```shell
pip install zeef
```

For the local development, you can install from the [Anaconda](https://www.anaconda.com/) environment by

```shell
conda env create -f environment.yml
```

## Quick Start

We can start from the easiest example: random select data points from an unlabeled data pool.

```python
from sklearn import svm

from zeef.data import Pool
from zeef.learner import SKLearner
from zeef.strategy import RandomSampling

learner = SKLearner(net=svm.SVC(probability=True))  # define the learner.
data_pool = Pool(unlabeled_data)  # generate the data pool.
strategy = RandomSampling(data_pool, learner=learner)  # define the sampling strategy.

query_ids = strategy.query(1000)  # query 1k samples for labeling.
strategy.update(query_ids, data_labels)  # label the 1k samples.
strategy.learn()  # train the model using all the labeled data.
strategy.infer(test_data)  # evaluate the model.
```

A quick MNIST CNN example can be found in [here](examples/mnist/main_torch.py). Run

```shell
python main_torch.py
```

to start the quick demonstration.

## License

[Apache License 2.0](./LICENSE)
