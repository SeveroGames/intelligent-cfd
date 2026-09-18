# tests/test_environment.py
import torch
import numpy as np

def test_numpy_installed():
    assert np.__version__ is not None

def test_pytorch_installed():
    assert torch.__version__ is not None