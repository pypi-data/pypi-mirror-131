import numpy
import copy
from maica.data_old.base import Dataset
from maica.data_old.util import get_split_idx


class GraphDataset(Dataset):
    """
    A base class to store the graph-structured data_old, such as the molecular and crystal structures.
    """

    def __init__(self,
                 data: list,
                 idx_struct: numpy.ndarray,
                 idx_feat: numpy.ndarray,
                 idx_target: int,
                 var_names: numpy.ndarray,
                 idx_data: numpy.ndarray = None):
        """
        :param data: (*list*) A list of ``torch_geometric.data_old.Data`` objects representing the structured data_old.
        :param idx_struct: (*numpy.ndarray*) Indices of the structured features in the dataset file.
        :param idx_feat: (*numpy.ndarray*) Indices of the numerical features in the dataset file.
        :param idx_target: (*int*) An index of the target value in the dataset file.
        :param var_names: (*numpy.ndarray*) Names of all variables in the dataset file.
        :param idx_data: (*numpy.ndarray*) Numerical indices of the data_old (*default* = ``None``).
        """

        super(GraphDataset, self).__init__(data, idx_feat, idx_target, var_names)

        # An index of the graph structure in the data_old file.
        self.idx_struct = copy.deepcopy(idx_struct)

        # Data object.
        self.x = data
        self.y = numpy.array([x[0].y.item() for x in self.data]) if self.contain_target else None
        self.idx_data = numpy.array([x[0].gid.item() for x in self.data])
        self.n_data = len(self.data)
        self.n_node_feats = self.data[0][0].x.shape[1]
        self.n_edge_feats = self.data[0][0].edge_attr.shape[1]
        self.n_graphs = len(self.data[0])

        # Information of data_old indexing.
        self.idx_data = numpy.arange(0, len(self.data)) if idx_data is None else copy.deepcopy(idx_data)

        # Initialize metadata of the dataset.
        if type(self).__name__ == 'GraphDataset':
            self._set_feat_names()
            self._set_tooltips()

    def _set_feat_names(self):
        """
        Set names and types of the input features.
        """

        for idx in self.idx_struct:
            self.feat_names.append(self.var_names[idx])
            self.feat_types.append('struct')

        if self.idx_feat is not None:
            for idx in self.idx_feat:
                self.feat_names.append(self.var_names[idx])
                self.feat_types.append('num')

    def _set_tooltips(self):
        """
        Set tooltip for each data_old to identify it in the data_old visualization.
        """

        for i in range(0, len(self.data)):
            self.tooltips.append('Data idx: ' + str(self.idx_data[i]))

    def split(self,
              ratio: float):
        """
        Split a dataset into two sub-datasets based on the given ratio.
        Two sub-datasets and the original indices of the data_old in them are returned.

        :param ratio: (*float*) Ratio between two sub-datasets. The sub-datasets are dived by a ratio of ``ratio`` to ``1 - ratio``.
        :return: (*maica.data_old.graph.GraphDataset, maica.data_old.graph.GraphDataset*) Two sub-datasets and the original indices of the data_old in them.
        """

        idx_dataset1, idx_dataset2 = get_split_idx(len(self.data), ratio)
        dataset1 = [self.data[idx] for idx in idx_dataset1]
        dataset2 = [self.data[idx] for idx in idx_dataset2]

        graph_dataset1 = GraphDataset(dataset1, self.idx_struct, self.idx_feat, self.idx_target,
                                      self.var_names, idx_dataset1)
        graph_dataset2 = GraphDataset(dataset2, self.idx_struct, self.idx_feat, self.idx_target,
                                      self.var_names, idx_dataset2)

        return graph_dataset1, graph_dataset2

    def get_sub_datasets(self,
                         k: int):
        """
        Split the dataset into the :math:`k` sub-datasets without repeating the data_old.
        In the training, :math:`k-1` sub-datasets are used to train the model, and the remaining sub-dataset is used for evaluation.

        :param k: (*int*) The number of subsets.
        :return: (*list*) A list of :math:`k` sub-datasets.
        """

        idx_rand = numpy.random.permutation(self.n_data)
        n_data_subset = int(self.n_data / k)
        sub_datasets = list()

        # Get k-1 sub-datasets with the same size.
        for i in range(0, k-1):
            idx_sub_dataset = idx_rand[i*n_data_subset:(i+1)*n_data_subset]
            dataset = [self.data[idx] for idx in idx_sub_dataset]
            sub_dataset = GraphDataset(dataset, self.idx_struct, self.idx_feat, self.idx_target,
                                       self.var_names, idx_sub_dataset)
            sub_datasets.append(sub_dataset)

        # Get the last sub-dataset containing the all remaining data_old.
        idx_sub_dataset = idx_rand[(k-1)*n_data_subset:]
        dataset = [self.data[idx] for idx in idx_sub_dataset]
        sub_dataset = GraphDataset(dataset, self.idx_struct, self.idx_feat, self.idx_target,
                                   self.var_names, idx_sub_dataset)
        sub_datasets.append(sub_dataset)

        return sub_datasets
