"""
    Basic PyTorch learner class for different platform.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 15/12/2021
"""

from tqdm import tqdm
from .base import Learner
from ..util.file_util import check_torch_version

try:
    import torch
    import torch.nn.functional as F
    from torch.utils.data import Dataset
    from torch.utils.data import DataLoader
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "No module named 'torch', and zeef PyTorch Learner class depends on PyTorch"
        "(aka 'torch'). "
        "Visit https://pytorch.org/ for installation instructions.")

check_torch_version()


class TorchDataset(Dataset):
    """
    TorchDataset: a base PyTorch dataset.
    Can process the input data, not with the input labels. The preprocessor is
    a single data point processing function that can be pickled.
    """

    def __init__(self, data_x, data_y, preprocessor=None):
        self.X = data_x
        self.Y = data_y
        self.processor = preprocessor

    def __getitem__(self, index):
        if self.processor is not None:
            x = self.processor(self.X[index])
        else:
            x = self.X[index]
        return x, self.Y[index], index

    def __len__(self):
        return len(self.X)


class TorchLearner(Learner):
    """
    The PyTorch implementation of base learner class.
    """

    def __init__(self, net, args, optimizer, criterion, transform=None, device=None):
        self.args = args  # TODO: needs refactor.
        self.net = net
        self.optimizer = optimizer
        self.criterion = criterion
        self.transform = transform
        if device:
            self.device = device
        else:  # initialize the dispatch device.
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def learn(self, data_x, data_y, n_epoch, batch_size, transform=None):
        """
        learn: to fit the pytorch model by given X and Y data.
        @param data_x: the training data.
        @param data_y: the corresponding labels of the training data (data_x).
        @param n_epoch: the training number of epoch.
        @param batch_size: the training batch size.
        @param transform: the data preprocessing method (if any). TODO: refactor make two transform together.
        @return: None.
        """
        loader_train = DataLoader(TorchDataset(data_x, data_y, transform), batch_size=batch_size)
        for _ in range(n_epoch):
            self.net.train()
            for _, (x, y, _) in tqdm(enumerate(loader_train)):
                x, y = x.to(self.device), y.to(self.device).type(torch.LongTensor)  # TODO: needs test (LongTensor)
                self.optimizer.zero_grad()
                out = self.net(x)
                loss = self.criterion(out, y)
                loss.backward()
                self.optimizer.step()

    def infer(self, data, batch_size, is_prob):
        """
        infer: inference function that returns the prediction results.
        @param data: the request data to perform inference.
        @param is_prob: the return values or probabilities.
        @param batch_size: the inference batch_size.
        @return: a list of inference results or a single result if given a single request.
        """
        outputs = []
        self.net.eval()
        if self.transform:
            data_x = self.transform(data)
        else:
            data_x = data
        batches = torch.split(data_x, batch_size)
        for batch in batches:
            batch = batch.to(self.device)
            with torch.no_grad():
                outputs.append(self.net(batch))
        outputs = torch.cat(outputs, dim=0)
        if is_prob:
            return F.softmax(outputs, dim=1).cpu().detach().numpy()
        else:
            return outputs.max(1)[1].cpu().detach().numpy()
