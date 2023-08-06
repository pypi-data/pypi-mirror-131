"""
Base Classes
------------
The ``maica.ml.base`` module includes basic classes of the machine learning algorithms.
It provides a wrapper class of the Scikit-learn models and an abstract class of the PyTorch models.
"""


import joblib
from abc import ABC
from abc import abstractmethod
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from gplearn.genetic import SymbolicRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct
from sklearn.gaussian_process.kernels import WhiteKernel
from xgboost import XGBRegressor
from maica.core.env import *
from maica.core.sys import *
from maica.data.base import NumericalDataset


class Model(ABC):
    @abstractmethod
    def __init__(self,
                 alg_name: str,
                 alg_src: str):
        self.__alg_name = ALG_CUSTOM if alg_name is None else alg_name
        self.__alg_src = alg_src
        self.__alg_desc = '<Algorithm: {}, Source library: {}>'.format(self.alg_name, self.alg_src)

    def __str__(self):
        return self.__alg_desc

    @property
    def alg_name(self):
        return self.__alg_name

    @property
    def alg_src(self):
        return self.__alg_src

    @property
    def alg_desc(self):
        return self.__alg_desc


class SKLearnModel(Model):
    def __init__(self,
                 alg_name: str = None,
                 **kwargs):
        super(SKLearnModel, self).__init__(alg_name, SRC_SKLEARN)
        self.__alg = None
        self.__init_model(**kwargs)

    def __init_model(self,
                     **kwargs):
        if self.alg_name == ALG_LR:
            # Linear Regression
            self.__alg = LinearRegression()
        elif self.alg_name == ALG_LASSO:
            # LASSO
            alpha = kwargs['alpha'] if 'alpha' in kwargs.keys() else 0.1
            self.__alg = Lasso(alpha=alpha)
        elif self.alg_name == ALG_DCTR:
            # Decision Tree Regression
            self.__alg = DecisionTreeRegressor()
        elif self.alg_name == ALG_SYMR:
            # Symbolic Regression
            population_size = kwargs['population_size'] if 'population_size' in kwargs.keys() else 1000
            generations = kwargs['generations'] if 'generations' in kwargs.keys() else 100
            p_subtree_mutation = kwargs['p_subtree_mutation'] if 'p_subtree_mutation' in kwargs.keys() else 0.01
            p_hoist_mutation = kwargs['p_hoist_mutation'] if 'p_hoist_mutation' in kwargs.keys() else 0.01
            p_point_mutation = kwargs['p_point_mutation'] if 'p_point_mutation' in kwargs.keys() else 0.01
            verbose = kwargs['verbose'] if 'verbose' in kwargs.keys() else 0
            self.__alg = SymbolicRegressor(population_size=population_size, generations=generations,
                                           p_subtree_mutation=p_subtree_mutation, p_hoist_mutation=p_hoist_mutation,
                                           p_point_mutation=p_point_mutation, verbose=verbose)
        elif self.alg_name == ALG_KRR:
            # Kernel Ridge Regression
            alpha = kwargs['alpha'] if 'alpha' in kwargs.keys() else 1.0
            self.__alg = KernelRidge(alpha=alpha)
        elif self.alg_name == ALG_KNNR:
            # K-Nearest Neighbor Regression
            n_neighbors = kwargs['n_neighbors'] if 'n_neighbors' in kwargs.keys() else 5
            self.__alg = KNeighborsRegressor(n_neighbors=n_neighbors)
        elif self.alg_name == ALG_GPR:
            # Gaussian Process Regression
            kernel = DotProduct() + WhiteKernel()
            self.__alg = GaussianProcessRegressor(kernel=kernel)
        elif self.alg_name == ALG_SVR:
            # Support Vector Regression
            c = kwargs['c'] if 'c' in kwargs.keys() else 1.0
            epsilon = kwargs['epsilon'] if 'epsilon' in kwargs.keys() else 0.1
            self.__alg = SVR(C=c, epsilon=epsilon)
        elif self.alg_name == ALG_GBTR:
            # Gradient Boosting Tree Regression
            max_depth = kwargs['max_depth'] if 'max_depth' in kwargs.keys() else 7
            n_estimators = kwargs['n_estimators'] if 'n_estimators' in kwargs.keys() else 300
            self.__alg = XGBRegressor(max_depth=max_depth, n_estimators=n_estimators)
        else:
            raise AssertionError('Unknown Scikit-learn model \'{}\' was given.'.format(self.alg_name))

    def fit(self,
            dataset: NumericalDataset):
        if dataset.contain_target:
            # Train the model with the supervision.
            self.__alg.fit(dataset.x, dataset.y)
        else:
            # Train the model without the supervision.
            self.__alg.fit(dataset.x)

    def predict(self,
                data: NumericalDataset):
        return self.__alg.predict(data.x).reshape(-1, 1)

    def save(self,
             path_model_file: str):
        joblib.dump(self.__alg, path_model_file)

    def load(self,
             path_model_file: str):
        self.__alg = joblib.load(path_model_file)


class PyTorchModel(torch.nn.Module, Model):
    @abstractmethod
    def __init__(self,
                 alg_name: str = None):
        torch.nn.Module.__init__(self)
        Model.__init__(self, alg_name, SRC_PYTORCH)

    @abstractmethod
    def forward(self,
                data: object):
        pass

    @abstractmethod
    def fit(self,
            data_loader: object,
            optimizer: torch.optim.Optimizer,
            criterion: object):
        pass

    @abstractmethod
    def predict(self,
                data: object):
        pass

    def save(self,
             path_model_file: str):
        torch.save(self.state_dict(), path_model_file)

    def load(self,
             path_model_file: str):
        self.load_state_dict(torch.load(path_model_file))
