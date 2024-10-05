import pytest
from challenge.cost_function import A, compute_cost_function
from challenge.model_params import K

import pandas as pd
import numpy as np


class TestCostFunction:
    def test_binary_encoding_lsd(self):
        """
        Test binary encoding on least significant digit
        Returns:

        """
        bit_string = [0] * (K-1) + [1]

        w = A(0, bit_string)

        assert w == 1/2**K

    def test_binary_encoding_msd(self):
        """
        Test binary encoding on most significant digit
        Returns:

        """
        bit_string = [1] + [0] * (K - 1)

        w = A(0, bit_string)

        assert w == 2 ** (K - 1) / 2**K

    def test_cost_fn(self, dataset, bitstring):
        H = compute_cost_function(dataset, bitstring)

        assert H is not None