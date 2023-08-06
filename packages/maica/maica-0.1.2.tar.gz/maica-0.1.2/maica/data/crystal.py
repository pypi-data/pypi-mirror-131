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
from maica.chem.crystal import get_crystal_graph


def load_crystal_graph_dataset(path_cif_files: str,
                               path_metadata_file: str,
                               idx_struct: object,
                               idx_feat: object = None,
                               idx_target: int = None,
                               impute_method: str = IMPUTE_KNN,
                               path_elem_embs: str = None,
                               dim_edge_feats: int = 64,
                               radius: float = 4.0):
    __idx_struct = numpy.atleast_1d(idx_struct)
    __idx_feat = None if idx_feat is None else numpy.atleast_1d(idx_feat)
    __idx_target = None if idx_target is None else numpy.atleast_1d(idx_target)
    elem_feats = load_elem_feats(path_elem_embs)
    data_file, data_obj = read_data_file(path_metadata_file)
    global_feats = None if __idx_feat is None else impute(data_obj[:, __idx_feat], impute_method)
    targets = None if idx_target is None else data_obj[:, __idx_target].astype(float)
    rbf_means = numpy.linspace(start=1.0, stop=radius, num=dim_edge_feats)
    data = list()

    for i in tqdm(range(0, data_obj.shape[0])):
        target = None if targets is None else targets[i]
        global_feats_crystal = None if global_feats is None else global_feats[i, :]
        crystal_graphs = list()

        for idx in __idx_struct:
            path_cif_file = path_cif_files + '/' + data_obj[i, idx] + '.cif'
            crystal_graph = get_crystal_graph(path_cif_file, elem_feats, rbf_means, global_feats=global_feats_crystal,
                                              target=target, radius=radius)
            crystal_graphs.append(crystal_graph)

        if None not in crystal_graphs:
            struct_id = ' '.join([data_obj[i, idx] for idx in __idx_struct])
            data.append(GraphData(x=crystal_graphs, y=target, idx=i, struct_id=struct_id))

    return GraphDataset(data, __idx_struct, __idx_feat, __idx_target, data_file.columns.values)
