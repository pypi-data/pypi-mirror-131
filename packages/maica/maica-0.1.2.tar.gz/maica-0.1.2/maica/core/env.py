"""
Environment Variables
---------------------
Environmental variables of MAICA is stored in this module.
The environmental variables are used to configure and transfer the datasets and the machine learning models.
This module must not be modified.
"""

# Feature Types
FEAT_TYPE_NUM = 'num'           # Numerical Value
FEAT_TYPE_FORM = 'form'         # Chemical Formula
FEAT_TYPE_STRUCT = 'struct'     # Mathematical Graph
FEAT_TYPE_IMG = 'img'           # Image


# Representation Method of Chemical Formula
REP_COMPACT = 'compact'         # Compact Representation
REP_SPARSE = 'sparse'           # Sparse Representation
REP_CONTENT = 'content'         # Content-Based Representation


# Imputation Methods of Missing Input Features
IMPUTE_MEAN = 'mean'            # Fill Empty Value by Mean
IMPUTE_ZERO = 'zero'            # Fill Empty Value by Zero
IMPUTE_KNN = 'knn'              # Fill Empty Value by K-Nearest Neighbor Data.


# Source Library of Machine Learning Algorithms
SRC_SKLEARN = 'Scikit-Learn'    # Scikit-Learn
SRC_PYTORCH = 'pyTorch'         # PyTorch


# Abbreviations of Machine Learning Algorithms
ALG_CUSTOM = 'User Defined Algorithm'
ALG_LR = 'Linear Regression'
ALG_LASSO = 'Lasso'
ALG_DCTR = 'Decision Tree Regression'
ALG_SYMR = 'Symbolic Regression'
ALG_KRR = 'Kernel Ridge Regression'
ALG_KNNR = 'K-Nearest Neighbor Regression'
ALG_SVR = 'Support Vector Regression'
ALG_GPR = 'Gaussian Process Regression'
ALG_GBTR = 'Gradient Boosting Tree Regression'
ALG_FNN = 'Feedforward Neural Network'
ALG_FCNN = 'Fully-Connected Neural Network'
ALG_DOPNET = 'DopNet'
ALG_ATE = 'Autoencoder'
ALG_GCN = 'Graph Convolutional Network'
ALG_GAT = 'Graph Attention Network'
ALG_GIN = 'Graph Isomorphism Network'
ALG_MPNN = 'Message Passing Neural Network'
ALG_CGCNN = 'Crystal Graph Convolutional Neural Network'
ALG_TFGNN = 'Transformer Graph Neural Network'


# List of Machine Learning Algorithms for Each Source Library.
ALGS_SKLEARN = [ALG_LR, ALG_LASSO, ALG_DCTR, ALG_SYMR, ALG_KRR, ALG_KNNR, ALG_SVR, ALG_GPR, ALG_GBTR]
ALGS_PYTORCH = [ALG_FCNN, ALG_ATE, ALG_DOPNET, ALG_GCN, ALG_GAT, ALG_GIN, ALG_MPNN, ALG_CGCNN, ALG_TFGNN]
ALGS_FNN = [ALG_FCNN, ALG_ATE, ALG_DOPNET]
ALGS_GNN = [ALG_GCN, ALG_GAT, ALG_GIN, ALG_MPNN, ALG_CGCNN, ALG_TFGNN]

# Gradient Descent Optimizers
GD_SGD = 'sgd'                  # Stochastic Gradient Descent Method
GD_ADADELTA = 'adadelta'        # AdaDelta Optimizer
GD_RMSPROP = 'rmsprop'          # Root Mean Square Propagation
GD_ADAM = 'adam'                # Adam Optimizer


# Loss Function
LOSS_MAE = 'mae'                # Mean Absolute Error
LOSS_MSE = 'mse'                # Mean Squared Error
LOSS_SMAE = 'smae'              # Smooth Mean Absolute Error


# Readout Methods for Graph Neural Networks
READOUT_MEAN = 'mean'           # Mean-Based Readout
READOUT_SUM = 'add'             # Sum-Based Readout


# Manifold Learning Methods
EMB_TSNE = 'tsne'               # t-Distributed Stochastic Neighbor Embedding
EMB_SPECT = 'spect'             # Spectral Embedding


# Optimization Types
PROB_MIN = 'min'                # Minimization Problem
PROB_MAX = 'max'                # Maximization Problem


# Metaheuristic Algorithms for Black-Box Optimization
OPT_EP = 'ep'                   # Evolutionary Programming
OPT_ES = 'es'                   # Evolution Strategies
OPT_MA = 'ma'                   # Memetic Algorithm
OPT_GA = 'ga'                   # Genetic Algorithm
OPT_DE = 'de'                   # Differential Evolution
OPT_FPA = 'fpa'                 # Flower Pollination Algorithm
OPT_CRO = 'cro'                 # Coral Reefs Optimization
OPT_PSO = 'pso'                 # Particle Swarm Optimization
OPT_BFO = 'bfo'                 # Bacterial Foraging Optimization
OPT_BEES = 'bees'               # Bees Algorithm
OPT_CSO = 'cso'                 # Cat Swarm Optimization
OPT_ACO = 'aco'                 # Ant Colony Optimization
OPT_ABC = 'abc'                 # Artificial Bee Colony
OPT_CSA = 'csa'                 # Cuckoo Search Algorithm
OPT_FFA = 'ffa'                 # Firefly Algorithm
OPT_FA = 'fa'                   # Fireworks Algorithm
OPT_BA = 'ba'                   # Bat Algorithm
OPT_FOA = 'foa'                 # Fruit-fly Optimization Algorithm
OPT_SSO = 'sso'                 # Social Spider Optimization
OPT_GWO = 'gwo'                 # Grey Wolf Optimizer
OPT_SSA = 'ssa'                 # Social Spider Algorithm
OPT_ALO = 'alo'                 # Ant Lion Optimizer
OPT_MFO = 'mfo'                 # Moth Flame Optimization
OPT_EHO = 'eho'                 # Elephant Herding Optimization
OPT_JA = 'ja'                   # Jaya Algorithm
OPT_WOA = 'woa'                 # Whale Optimization Algorithm
OPT_DO = 'do'                   # Dragonfly Optimization
OPT_BSA = 'bsa'                 # Bird Swarm Algorithm
OPT_SHO = 'sho'                 # Spotted Hyena Optimizer
OPT_SALP = 'salp'               # Salp Swarm Optimization
OPT_SRSR = 'srsr'               # Swarm Robotics Search And Rescue
OPT_GOA = 'goa'                 # Grasshopper Optimization Algorithm
OPT_MSA = 'msa'                 # Moth Search Algorithm
OPT_SLO = 'slo'                 # Sea Lion Optimization
OPT_NMRA = 'nmra'               # Nake Mole-rat Algorithm
OPT_BES = 'bes'                 # Bald Eagle Search
OPT_PFA = 'pfa'                 # Pathfinder Algorithm
OPT_SFO = 'sfo'                 # Sailfish Optimizer
OPT_HHO = 'hho'                 # Harris Hawks Optimization
OPT_MRFO = 'mrfo'               # Manta Ray Foraging Optimization
OPT_SPA = 'spa'                 # Sparrow Search Algorithm
OPT_HGS = 'hgs'                 # Hunger Games Search
OPT_AO = 'ao'                   # Aquila Optimizer
OPT_SA = 'sa'                   # Simulated Annealing
OPT_WDO = 'wdo'                 # Wind Driven Optimization
OPT_MVO = 'mvo'                 # Multi-Verse Optimizer
OPT_TWO = 'two'                 # Tug of War Optimization
OPT_EFO = 'efo'                 # Electromagnetic Field Optimization
OPT_NRO = 'nro'                 # Nuclear Reaction Optimization
OPT_HGSO = 'hgso'               # Henry Gas Solubility Optimization
OPT_ASO = 'aso'                 # Atom Search Optimization
OPT_EO = 'eo'                   # Equilibrium Optimizer
OPT_ARCH = 'arch'               # Archimedes Optimization Algorithm
OPT_CA = 'ca'                   # Culture Algorithm
OPT_ICA = 'ica'                 # Imperialist Competitive Algorithm
OPT_TLO = 'tlo'                 # Teaching Learning Optimization
OPT_BSO = 'bso'                 # Brain Storm Optimization
OPT_QSA = 'qsa'                 # Queuing Search Algorithm
OPT_SARO = 'saro'               # Search And Rescue Optimization
OPT_LCBO = 'lcbo'               # Life Choice-Based Optimization
OPT_SSDO = 'ssdo'               # Social Ski-Driver Optimization
OPT_GSKA = 'gska'               # Gaining Sharing Knowledge-based Algorithm
OPT_CHIO = 'chio'               # Coronavirus Herd Immunity Optimization
OPT_FBIO = 'fbio'               # Forensic-Based Investigation Optimization
OPT_BRO = 'bro'                 # Battle Royale Optimization
OPT_IWO = 'iwo'                 # Invasive Weed Optimization
OPT_BBO = 'bbo'                 # Biogeography-Based Optimization
OPT_VCS = 'vcs'                 # Virus Colony Search
OPT_SBO = 'sbo'                 # Satin Bowerbird Optimizer
OPT_EOA = 'eoa'                 # Earthworm Optimisation Algorithm
OPT_WHO = 'who'                 # Wildebeest Herd Optimization
OPT_SMA = 'sma'                 # Slime Mould Algorithm
OPT_GCO = 'gco'                 # Germinal Center Optimization
OPT_WCA = 'wca'                 # Water Cycle Algorithm
OPT_AEO = 'aeo'                 # Artificial Ecosystem-based Optimization
OPT_HC = 'hc'                   # Hill Climbing
OPT_SCA = 'sca'                 # Sine Cosine Algorithm
OPT_AOA = 'aoa'                 # Arithmetic Optimization Algorithm
OPT_HS = 'hs'                   # Harmony Search
OPT_CEM = 'cem'                 # Cross-Entropy Method
OPT_PIO = 'pio'                 # Pigeon-Inspired Optimization
OPT_AAA = 'aaa'                 # Artificial Algae Algorithm
OPT_RHO = 'rho'                 # Rhino Herd Optimization
OPT_EPO = 'epo'                 # Emperor Penguin Optimizer
OPT_BOA = 'boa'                 # Butterfly Optimization Algorithm
OPT_BMO = 'bmo'                 # Blue Monkey Optimization
OPT_SOA = 'soa'                 # Sandpiper Optimization Algorithm
OPT_BWO = 'bwo'                 # Black Widow Optimization
