"""
Feedforward Neural Networks
---------------------------
The ``maica.ml.fnn`` module provides an implementation of the most essential feedforward neural network.
The algorithms in this module are used to predict target values from the feature vectors and the chemical formulas.
"""


import torch.utils.data
import torch.nn as nn
import torch.nn.functional as F
from abc import abstractmethod
from maica.core.env import *
from maica.core.sys import *
from maica.data.base import NumericalData
from maica.ml.base import PyTorchModel
from maica.ml.embedding import Autoencoder


class FNN(PyTorchModel):
    @abstractmethod
    def __init__(self,
                 alg_name: str):
        super(FNN, self).__init__(alg_name)

    @abstractmethod
    def forward(self,
                data: object):
        pass

    def fit(self,
            data_loader: torch.utils.data.DataLoader,
            optimizer: torch.optim.Optimizer,
            criterion: torch.nn.Module):
        self.train()
        train_loss = 0

        for inputs, targets in data_loader:
            if is_gpu_runnable():
                inputs = inputs.cuda()
                targets = targets.cuda()

            preds = self(inputs)
            loss = criterion(preds, targets)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        return train_loss / len(data_loader)

    def predict(self,
                data: NumericalData):
        self.eval()

        with torch.no_grad():
            __data = torch.tensor(data.x, dtype=torch.float) if isinstance(data.x, numpy.ndarray) else data.x

            if is_gpu_runnable():
                return self(__data.cuda()).cpu().numpy()
            else:
                return self(__data).numpy()


class FCNN(FNN):
    def __init__(self,
                 dim_input: int,
                 dim_target: int):
        super(FCNN, self).__init__(ALG_FCNN)
        self.fc1 = nn.Linear(dim_input, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.fc3 = nn.Linear(256, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.fc4 = nn.Linear(32, dim_target)

    def forward(self,
                x: torch.tensor):
        h = F.relu(self.bn1(self.fc1(x)))
        h = F.relu(self.bn2(self.fc2(h)))
        h = F.relu(self.bn3(self.fc3(h)))
        out = self.fc4(h)

        return out


class DopNet(FNN):
    def __init__(self,
                 dim_input_host: int,
                 dim_input_dop: int,
                 dim_emb_host: int,
                 dim_target: int):
        super(DopNet, self).__init__(ALG_DOPNET)
        self.dim_input_host = dim_input_host
        self.emb_net = Autoencoder(dim_input=dim_input_host, dim_latent=dim_emb_host)
        self.pred_net = FCNN(dim_input=dim_emb_host+dim_input_dop, dim_target=dim_target)

    def forward(self,
                x: torch.tensor):
        host_embs = self.emb_net.enc(x[:, :self.dim_input_host])
        out = self.pred_net(torch.cat([host_embs, x[:, self.dim_input_host:]], dim=1))

        return out

    def fit_emb_net(self,
                    data_loader: torch.utils.data.DataLoader,
                    optimizer: torch.optim.Optimizer,
                    criterion: torch.nn.Module):
        self.train()
        train_loss = 0

        for inputs, _ in data_loader:
            __inputs = inputs[:, :self.dim_input_host]

            if is_gpu_runnable():
                __inputs = __inputs.cuda()

            preds = self.emb_net(__inputs)
            loss = criterion(__inputs, preds)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        return train_loss / len(data_loader)
