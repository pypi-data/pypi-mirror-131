import torch.utils.data as tdata
import torch_geometric.data as tgdata
import sklearn.metrics as metrics
from maica.ml.base import *
from maica.ml.fnn import *
from maica.ml.embedding import *
from maica.ml.gnn import *
from maica.core.sys import is_gpu_runnable
from maica.data.base import Dataset
from maica.data.base import GraphDataset


def get_model(alg_name: str,
              **kwargs):
    if alg_name in ALGS_SKLEARN:
        # Scikit-learn Algorithms
        return SKLearnModel(alg_name, **kwargs)
    elif alg_name in ALGS_PYTORCH:
        # Pytorch Algorithms
        readout_method = kwargs['readout_method'] if 'readout_method' in kwargs.keys() else None

        if alg_name == ALG_FCNN:
            model = FCNN(dim_input=kwargs['dim_input'], dim_target=kwargs['dim_target'])
        elif alg_name == ALG_DOPNET:
            model = DopNet(dim_input_host=kwargs['dim_input_host'], dim_input_dop=kwargs['dim_input_dop'],
                           dim_emb_host=kwargs['dim_emb_host'], dim_target=kwargs['dim_target'])
        elif alg_name == ALG_ATE:
            model = Autoencoder(dim_input=kwargs['dim_input'], dim_latent=kwargs['dim_latent'])
        elif alg_name == ALG_GCN:
            model = GCN(dim_input_node=kwargs['dim_input_node'], n_structs=kwargs['n_structs'],
                        dim_target=kwargs['dim_target'], readout_method=readout_method)
        elif alg_name == ALG_GAT:
            model = GAT(dim_input_node=kwargs['dim_input_node'], n_structs=kwargs['n_structs'],
                        dim_target=kwargs['dim_target'], readout_method=readout_method)
        elif alg_name == ALG_GIN:
            model = GIN(dim_input_node=kwargs['dim_input_node'], n_structs=kwargs['n_structs'],
                        dim_target=kwargs['dim_target'], readout_method=readout_method)
        elif alg_name == ALG_MPNN:
            model = MPNN(dim_input_node=kwargs['dim_input_node'], dim_input_edge=kwargs['dim_input_edge'],
                         n_structs=kwargs['n_structs'], dim_target=kwargs['dim_target'],
                         readout_method=readout_method)
        elif alg_name == ALG_CGCNN:
            model = CGCNN(dim_input_node=kwargs['dim_input_node'], dim_input_edge=kwargs['dim_input_edge'],
                          n_structs=kwargs['n_structs'], dim_target=kwargs['dim_target'],
                          readout_method=readout_method)
        elif alg_name == ALG_TFGNN:
            model = TFGNN(dim_input_node=kwargs['dim_input_node'], dim_input_edge=kwargs['dim_input_edge'],
                          n_structs=kwargs['n_structs'], dim_target=kwargs['dim_target'],
                          readout_method=readout_method)
        else:
            AssertionError('Unknown algorithm \'{}\' was given. Check available algorithms in \'maica.core.env\'.'
                           .format(alg_name))

        if is_gpu_runnable():
            model.cuda()

        return model
    else:
        raise AssertionError('Unknown algorithm \'{}\' was given. Check available algorithms in \'maica.core.env\'.'
                             .format(alg_name))


def get_data_loader(dataset: Dataset,
                    batch_size: int = 8,
                    shuffle: bool = False):
    if isinstance(dataset, GraphDataset):
        return tgdata.DataLoader(dataset.x, batch_size=batch_size, shuffle=shuffle)
    else:
        dataset.to_tensor()

        if dataset.contain_target:
            tensors = [dataset.x, dataset.y]
        else:
            tensors = [dataset.x]

        return tdata.DataLoader(tdata.TensorDataset(*tuple(tensors)), batch_size=batch_size, shuffle=shuffle)


def get_optimizer(model_params: torch.Generator,
                  gd_name: str,
                  init_lr: float = 1e-3,
                  l2_reg: float = 1e-6):
    if gd_name == GD_SGD:
        return torch.optim.SGD(model_params, lr=init_lr, weight_decay=l2_reg, momentum=0.9)
    elif gd_name == GD_ADADELTA:
        return torch.optim.Adadelta(model_params, lr=init_lr, weight_decay=l2_reg)
    elif gd_name == GD_RMSPROP:
        return torch.optim.RMSprop(model_params, lr=init_lr, weight_decay=l2_reg)
    elif gd_name == GD_ADAM:
        return torch.optim.Adam(model_params, lr=init_lr, weight_decay=l2_reg)
    else:
        raise AssertionError('Unknown gradient method {} was given.'.format(gd_name))


def get_loss_func(loss_func: str):
    if loss_func == LOSS_MAE:
        return torch.nn.L1Loss()
    elif loss_func == LOSS_MSE:
        return torch.nn.MSELoss()
    elif loss_func == LOSS_SMAE:
        return torch.nn.SmoothL1Loss()
    else:
        raise AssertionError('Unknown loss function {} was given.'.format(loss_func))


def mae(targets: numpy.ndarray,
        preds: numpy.ndarray):
    return metrics.mean_absolute_error(targets, preds)


def rmse(targets: numpy.ndarray,
         preds: numpy.ndarray):
    return numpy.sqrt(metrics.mean_squared_error(targets, preds))


def r2_score(targets: numpy.ndarray,
             preds: numpy.ndarray):
    return metrics.r2_score(targets, preds)
