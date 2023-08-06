"""
System Utilities
----------------
This module contains essential functions to check or set the configuration of the package and the machine.
"""


import random
import numpy
import torch
import warnings


# Ignore unnecessary warnings from third party packages.
warnings.filterwarnings(action='ignore', category=UserWarning)

# Global configurations of machine learning algorithms.
run_gpu = False


def set_gpu_runnable(runnable: bool):
    """
    Set GPU enable for running machine learning algorithm in GPU.

    :param runnable: A flag to indicate the GPU enable.

    Example:

    >>> set_gpu_runnable(True) # Enable GPU.
    """

    if torch.cuda.is_available():
        global run_gpu
        run_gpu = runnable
    else:
        raise AssertionError('GPU is not available in your machine.'
                             'Make sure the CUDA Driver is installed in the system.')


def set_random_seed(seed: int):
    """
    Set the random seed of the program.
    It can be used to provided a reproducible experiment scripts.

    :param seed: An integer index of the random seed.
    """

    random.seed(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)


def is_gpu_runnable():
    """
    Check GPU is runnable in the machine.
    If GPU is available, ``True`` is returned.

    :return: (*bool*) A flag indicating GPU availability.
    """

    return run_gpu
