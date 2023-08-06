"""
Graph Neural Networks
---------------------
The ``maica.ml.gnn`` module provides an implementation of the most essential feedforward neural network.
The algorithms in this module are used to predict target values from the feature vectors and the chemical formulas.
"""


import torch.utils.data
import torch.nn as nn
from abc import abstractmethod
from torch_geometric.data import DataLoader
from torch_geometric.nn import Sequential
from torch_geometric.nn import LayerNorm
from torch_geometric.nn import GCNConv
from torch_geometric.nn import GATConv
from torch_geometric.nn import GINConv
from torch_geometric.nn import NNConv
from torch_geometric.nn import CGConv
from torch_geometric.nn import TransformerConv
from torch_geometric.nn import global_mean_pool
from torch_geometric.nn import global_add_pool
from maica.core.env import *
from maica.core.sys import *
from maica.data.base import GraphData
from maica.ml.base import PyTorchModel


def batch_to_gpu(batches: list):
    for batch in batches:
        batch.x = batch.x.cuda()
        batch.y = batch.y.cuda()
        batch.edge_index = batch.edge_index.cuda()
        batch.batch = batch.batch.cuda()
        batch.edge_attr = None if batch.edge_attr is None else batch.edge_attr.cuda()


class GNN(PyTorchModel):
    @abstractmethod
    def __init__(self,
                 alg_name: str,
                 dim_input_node: int,
                 n_structs: int,
                 dim_target: int,
                 dim_input_edge: int,
                 readout_method: str):
        super(GNN, self).__init__(alg_name)
        self.aggr_layers = None
        self.pred_layers = None
        self.__dim_input_node = dim_input_node
        self.__dim_input_edge = dim_input_edge
        self.__n_structs = n_structs
        self.__dim_target = dim_target
        self.__dim_input_edge = dim_input_edge
        self.__readout_method = readout_method

    @property
    def dim_input_node(self):
        return self.__dim_input_node

    @property
    def dim_input_edge(self):
        return self.__dim_input_edge

    @property
    def n_structs(self):
        return self.__n_structs

    @property
    def dim_target(self):
        return self.__dim_target

    @property
    def readout_method(self):
        return self.__readout_method

    def forward(self,
                data: list):

        if self.dim_input_edge is None:
            h = [self.aggr_layers(g.x, g.edge_index) for g in data]
        else:
            h = [self.aggr_layers(g.x, g.edge_index, g.edge_attr) for g in data]

        if self.readout_method is None:
            h = torch.hstack(h)
        else:
            h = torch.hstack([self.readout(h[i], data[i].batch) for i in range(0, self.n_structs)])

        out = self.pred_layers(h)

        return out

    def readout(self,
                node_embs: torch.Tensor,
                batch_idx: torch.Tensor):
        if self.readout_method == READOUT_MEAN:
            return global_mean_pool(node_embs, batch_idx)
        elif self.readout_method == READOUT_SUM:
            return global_add_pool(node_embs, batch_idx)
        else:
            raise AssertionError('Unknown readout method {}.'.format(self.readout))

    def fit(self,
            data_loader: torch.utils.data.DataLoader,
            optimizer: torch.optim.Optimizer,
            criterion: torch.nn.Module):
        self.train()
        train_loss = 0

        for batches in data_loader:
            if is_gpu_runnable():
                batch_to_gpu(batches)

            preds = self(batches)
            loss = criterion(batches[0].y, preds)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.detach().item()

        return train_loss / len(data_loader)

    def predict(self,
                data: GraphData):
        self.eval()
        __graphs = list(data.x) if isinstance(data, GraphData) else data.x
        data_loader = DataLoader(__graphs, batch_size=128)
        list_preds = list()

        with torch.no_grad():
            for batches in data_loader:
                if is_gpu_runnable():
                    batch_to_gpu(batches)
                    list_preds.append(self(batches).cpu())
                else:
                    list_preds.append(self(batches))

        return torch.vstack(list_preds).numpy()


class GCN(GNN):
    def __init__(self,
                 dim_input_node: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(GCN, self).__init__(ALG_GCN, dim_input_node, n_structs, dim_target, None, readout_method)
        self.aggr_layers = Sequential('x, edge_index', [
            (GCNConv(self.dim_input_node, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GCNConv(256, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GCNConv(256, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 256, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )


class GAT(GNN):
    def __init__(self,
                 dim_input_node: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(GAT, self).__init__(ALG_GAT, dim_input_node, n_structs, dim_target, None, readout_method)
        self.aggr_layers = Sequential('x, edge_index', [
            (GATConv(self.dim_input_node, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GATConv(256, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GATConv(256, 256), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 256, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )


class GIN(GNN):
    def __init__(self,
                 dim_input_node: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(GIN, self).__init__(ALG_GIN, dim_input_node, n_structs, dim_target, None, readout_method)
        self.aggr_layers = Sequential('x, edge_index', [
            (GINConv(nn.Linear(self.dim_input_node, 256)), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GINConv(nn.Linear(256, 256)), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (GINConv(nn.Linear(256, 256)), 'x, edge_index -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 256, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )


class MPNN(GNN):
    def __init__(self,
                 dim_input_node: int,
                 dim_input_edge: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(MPNN, self).__init__(ALG_MPNN, dim_input_node, n_structs, dim_target, dim_input_edge, readout_method)
        self.nn1 = nn.Sequential(
            nn.Linear(self.dim_input_edge, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_input_node * 128)
        )
        self.nn2 = nn.Sequential(
            nn.Linear(self.dim_input_edge, 64),
            nn.ReLU(),
            nn.Linear(64, 128 * 64)
        )
        self.nn3 = nn.Sequential(
            nn.Linear(self.dim_input_edge, 64),
            nn.ReLU(),
            nn.Linear(64, 64 * 64)
        )
        self.aggr_layers = Sequential('x, edge_index, edge_attr', [
            (NNConv(self.dim_input_node, 128, self.nn1), 'x, edge_index, edge_attr -> x'),
            LayerNorm(128),
            nn.ReLU(inplace=True),
            (NNConv(128, 64, self.nn2), 'x, edge_index, edge_attr -> x'),
            LayerNorm(64),
            nn.ReLU(inplace=True),
            (NNConv(64, 64, self.nn3), 'x, edge_index, edge_attr -> x'),
            LayerNorm(64),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 64, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )


class CGCNN(GNN):
    def __init__(self,
                 dim_input_node: int,
                 dim_input_edge: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(CGCNN, self).__init__(ALG_CGCNN, dim_input_node, n_structs, dim_target, dim_input_edge, readout_method)
        self.aggr_layers = Sequential('x, edge_index, edge_attr', [
            (nn.Linear(self.dim_input_node, 256), 'x -> x'),
            (CGConv(256, self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (CGConv(256, self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (CGConv(256, self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 256, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )


class TFGNN(GNN):
    def __init__(self,
                 dim_input_node: int,
                 dim_input_edge: int,
                 n_structs: int,
                 dim_target: int,
                 readout_method: str = None):
        super(TFGNN, self).__init__(ALG_TFGNN, dim_input_node, n_structs, dim_target, dim_input_edge, readout_method)
        self.aggr_layers = Sequential('x, edge_index, edge_attr', [
            (TransformerConv(self.dim_input_node, 256, edge_dim=self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (TransformerConv(256, 256, edge_dim=self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True),
            (TransformerConv(256, 256, edge_dim=self.dim_input_edge), 'x, edge_index, edge_attr -> x'),
            LayerNorm(256),
            nn.ReLU(inplace=True)
        ])
        self.pred_layers = nn.Sequential(
            nn.Linear(self.n_structs * 256, 64),
            nn.ReLU(),
            nn.Linear(64, self.dim_target)
        )
