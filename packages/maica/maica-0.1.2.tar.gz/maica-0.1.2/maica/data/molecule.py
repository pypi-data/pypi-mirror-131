"""
Molecular Structure
-------------------
This module provides several utilities to handle the datasets containing the molecular structures.
You can load a dataset containing the molecular structures to the ``maica.data_old.graph.GraphDataset`` object
by calling ``load_dataset`` function in this module.
"""


import numpy
from tqdm import tqdm
from maica.core.env import *
from maica.data.base import GraphData
from maica.data.base import GraphDataset
from maica.data.util import read_data_file
from maica.data.util import impute
from maica.chem.base import load_elem_feats
from maica.chem.molecule import get_mol_graph


def load_mol_graph_dataset(path_metadata_file: str,
                           idx_struct: object,
                           idx_feat: object = None,
                           idx_target: int = None,
                           impute_method: str = IMPUTE_KNN,
                           path_elem_embs: str = None,
                           present_hydrogen = False):
    __idx_struct = numpy.atleast_1d(idx_struct)
    __idx_feat = None if idx_feat is None else numpy.atleast_1d(idx_feat)
    __idx_target = None if idx_target is None else numpy.atleast_1d(idx_target)
    elem_feats = load_elem_feats(path_elem_embs)
    data_file, data_obj = read_data_file(path_metadata_file)
    global_feats = None if __idx_feat is None else impute(data_obj[:, __idx_feat], impute_method)
    targets = None if __idx_target is None else data_obj[:, __idx_target].astype(float)
    data = list()

    for i in tqdm(range(0, data_obj.shape[0])):
        target = None if targets is None else targets[i]
        global_feats_mol = None if global_feats is None else global_feats[i, :]
        mol_graphs = [get_mol_graph(data_obj[i, idx], elem_feats, global_feats=global_feats_mol, target=target,
                                    present_hydrogen=present_hydrogen) for idx in __idx_struct]

        if None not in mol_graphs:
            struct_id = ' '.join([data_obj[i, idx] for idx in __idx_struct])
            data.append(GraphData(x=mol_graphs, y=target, idx=i, struct_id=struct_id))

    return GraphDataset(data, __idx_struct, __idx_feat, __idx_target, data_file.columns.values)
