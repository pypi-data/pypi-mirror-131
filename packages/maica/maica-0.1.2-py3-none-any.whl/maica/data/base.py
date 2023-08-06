import numpy
import copy
import torch
from abc import ABC
from abc import abstractmethod
from sklearn.neighbors import LocalOutlierFactor
from maica.core.env import *
from maica.data.util import get_sub_list


class Data:
    def __init__(self,
                 x: object,
                 y: object,
                 idx: int):
        self.x = copy.deepcopy(x)
        self.y = None if y is None else copy.deepcopy(y)
        self._idx = idx
        self._tooltip = 'Data index: {}'.format(self.idx)

    def __str__(self):
        return '<{} index: {}, x: {}, y: {}>'.format(type(self).__name__, str(self.idx), str(self.x), str(self.y))

    @property
    def idx(self):
        return self._idx

    @property
    def tooltip(self):
        return self._tooltip


class NumericalData(Data):
    def __init__(self,
                 x: object,
                 y: object,
                 idx: int):
        super(NumericalData, self).__init__(x, y, idx)

    def to_numpy(self):
        self.x = self.x.numpy()

        if self.y is not None:
            self.y = self.y.numpy()

    def to_tensor(self):
        self.x = torch.tensor(self.x, dtype=torch.float)

        if self.y is not None:
            self.y = torch.tensor(self.y, dtype=torch.float)


class GraphData(Data):
    def __init__(self,
                 x: list,
                 y: object,
                 idx: int,
                 struct_id: str):
        super(GraphData, self).__init__(x, y, idx)
        self._tooltip += ', Structure Id: {}'.format(struct_id)
        self.__dim_input_node = x[0].x.shape[1]
        self.__dim_input_edge = None if x[0].edge_attr is None else x[0].edge_attr.shape[1]
        self.__struct_id = copy.deepcopy(struct_id)

    def __str__(self):
        return '<{}, index: {}, structure id: {}, x: {}, y: {}>'.\
            format(type(self).__name__, str(self.idx), self.struct_id, str(self.x), str(self.y))

    @property
    def dim_input_node(self):
        return self.__dim_input_node

    @property
    def dim_input_edge(self):
        return self.__dim_input_edge

    @property
    def struct_id(self):
        return self.__struct_id


class Dataset(ABC):
    @abstractmethod
    def __init__(self,
                 data: list,
                 idx_feat: numpy.ndarray,
                 idx_target: numpy.ndarray,
                 var_names: numpy.ndarray):
        self.data = copy.deepcopy(data)
        self.x = self._collect_input_data()
        self.y = None if idx_target is None else self._collect_target_data()

        # Initialize metadata of the dataset.
        self.__idx_feat = copy.deepcopy(idx_feat)
        self.__idx_target = None if idx_target is None else copy.deepcopy(idx_target)
        self.__contain_target = False if self.idx_target is None else True
        self.__var_names = copy.deepcopy(var_names)
        self.__target_name = None if self.__idx_target is None else self.var_names[self.__idx_target]
        self._n_data = len(data)
        self._dim_input = None
        self._dim_target = None if self.y is None else self.y.shape[1]
        self._feat_names = list()
        self._feat_types = list()
        self._tooltips = self._collect_tooltips()

    @property
    def idx_feat(self):
        return self.__idx_feat

    @property
    def idx_target(self):
        return self.__idx_target

    @property
    def contain_target(self):
        return self.__contain_target

    @property
    def var_names(self):
        return self.__var_names

    @property
    def target_name(self):
        return self.__target_name

    @property
    def n_data(self):
        return self._n_data

    @property
    def dim_input(self):
        return self._dim_input

    @property
    def dim_target(self):
        return self._dim_target

    @property
    def feat_names(self):
        return self._feat_names

    @property
    def feat_types(self):
        return self._feat_types

    @property
    def tooltips(self):
        return self._tooltips

    @abstractmethod
    def _set_feat_info(self):
        pass

    @abstractmethod
    def _update_data(self, new_data):
        pass

    @abstractmethod
    def _collect_input_data(self):
        pass

    def _update_target_data(self):
        self.y = self._collect_target_data()

    def _collect_target_data(self):
        if isinstance(self.data[0].y, numpy.ndarray):
            return numpy.vstack([d.y for d in self.data])
        elif isinstance(self.data[0].y, torch.Tensor):
            return torch.vstack([d.y for d in self.data])
        else:
            raise AssertionError('Unknown data type of the target data.')

    def _collect_tooltips(self):
        return [d.tooltip for d in self.data]

    def clone(self):
        return copy.deepcopy(self)

    def split(self,
              ratio: float):
        if ratio >= 1 or ratio <= 0:
            raise AssertionError('The radio must be in [0, 1], but the given ratio is {:.4f}'.format(ratio))

        n_dataset1 = int(ratio * self.n_data)
        idx_rand = numpy.random.permutation(self.n_data)
        idx_dataset1 = idx_rand[:n_dataset1]
        idx_dataset2 = idx_rand[n_dataset1:]

        # Clone the dataset objects.
        dataset1 = self.clone()
        dataset2 = self.clone()

        # Update the sub-datasets with the sampled sub-data.
        dataset1._update_data(get_sub_list(self.data, idx_dataset1))
        dataset2._update_data(get_sub_list(self.data, idx_dataset2))

        return dataset1, dataset2

    def get_k_folds(self,
                    k: int):
        idx_rand = numpy.random.permutation(self.n_data)
        n_data_subset = int(self.n_data / k)
        sub_datasets = list()

        # Get k-1 sub-datasets with the same size.
        for i in range(0, k-1):
            idx_sub_dataset = idx_rand[i*n_data_subset:(i+1)*n_data_subset]
            sub_dataset = self.clone()
            sub_dataset._update_data(get_sub_list(self.data, idx_sub_dataset))
            sub_datasets.append(sub_dataset)

        # Get the last sub-dataset containing all remaining data.
        idx_sub_dataset = idx_rand[(k-1)*n_data_subset:]
        sub_dataset = self.clone()
        sub_dataset._update_data(get_sub_list(self.data, idx_sub_dataset))
        sub_datasets.append(sub_dataset)

        return sub_datasets


class NumericalDataset(Dataset):
    @abstractmethod
    def __init__(self,
                 data: list,
                 idx_feat: object,
                 idx_target: int,
                 var_names: numpy.ndarray):
        super(NumericalDataset, self).__init__(data, idx_feat, idx_target, var_names)
        self._dim_input = self.x.shape[1]
        self._feat_means = None
        self._feat_stds = None

    @property
    def feat_means(self):
        return self._feat_means

    @property
    def feat_stds(self):
        return self._feat_stds

    @abstractmethod
    def _set_feat_info(self):
        pass

    def _update_data(self, new_data):
        self.data = copy.deepcopy(new_data)
        self._tooltips = self._collect_tooltips()
        self._n_data = len(self.data)
        self._update_input_data()

        if self.contain_target:
            self._update_target_data()

    def _update_input_data(self):
        self.x = self._collect_input_data()

    def _collect_input_data(self):
        if isinstance(self.data[0].x, numpy.ndarray):
            return numpy.vstack([d.x for d in self.data])
        elif isinstance(self.data[0].x, torch.Tensor):
            return torch.vstack([d.x for d in self.data])
        else:
            raise AssertionError('Unknown data type of the input data.')

    def to_numpy(self):
        for i in range(0, self.n_data):
            self.data[i].to_numpy()
        self._update_input_data()
        self._update_target_data()

    def to_tensor(self):
        for i in range(0, self.n_data):
            self.data[i].to_tensor()
        self._update_input_data()

        if self.contain_target:
            self._update_target_data()

    def remove_outliers(self):
        if not isinstance(self.x, numpy.ndarray):
            raise AssertionError('Outlier removal is supported only for numpy.ndarray object. '
                                 'Call to_numpy() method before executing this method.')

        lof = LocalOutlierFactor(n_neighbors=int(numpy.sqrt(self.n_data)))
        ind = lof.fit_predict(self.x)

        new_data = [self.data[i] for i in range(0, self.n_data) if ind[i] == 1]
        self._update_data(new_data)


class GraphDataset(Dataset):
    def __init__(self,
                 data: list,
                 idx_struct: object,
                 idx_feat: object,
                 idx_target: int,
                 var_names: numpy.ndarray):
        super(GraphDataset, self).__init__(data, idx_feat, idx_target, var_names)
        self.__dim_input_node = self.data[0].dim_input_node
        self.__dim_input_edge = self.data[0].dim_input_edge
        self.__n_structs = len(self.data[0].x)
        self.__idx_struct = copy.deepcopy(idx_struct)

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
    def idx_struct(self):
        return self.__idx_struct

    def _set_feat_info(self):
        for idx in self.idx_struct:
            self._feat_names.append(self.var_names[idx])
            self._feat_types.append(FEAT_TYPE_STRUCT)

        for idx in self.idx_feat:
            self._feat_names.append(self.var_names[idx])
            self._feat_types.append(FEAT_TYPE_NUM)

    def _update_data(self, new_data):
        self.data = copy.deepcopy(new_data)
        self._tooltips = self._collect_tooltips()
        self._n_data = len(self.data)
        self._update_input_data()

        if self.contain_target:
            self._update_target_data()

    def _update_input_data(self):
        self.x = self._collect_input_data()

    def _collect_input_data(self):
        return [d.x for d in self.data]
