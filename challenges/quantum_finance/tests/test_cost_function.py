import pytest
from cost_function import A
from model_params import K


class TestCostFunction:
    def test_binary_encoding_lsd(self):
        """
        Test binary encoding on least significant digit
        Returns:

        """
        bit_string = [1] * (K-1) + [-1]

        w = A(0, bit_string)

        assert w == 1/2**K

    def test_binary_encoding_msd(self):
        """
        Test binary encoding on most significant digit
        Returns:

        """
        bit_string = [-1] + [1] * (K - 1)

        w = A(0, bit_string)

        assert w == 2 ** (K - 1) / 2**K
