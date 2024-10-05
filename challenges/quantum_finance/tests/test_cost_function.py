import pytest
from challenge.cost_function import A, compute_cost_function
from challenge.model_params import K

import pandas as pd
import numpy as np


def generate_gaussian_dataframe(n_rows: int, n_columns: int):
    # Create date range for index
    date_index = pd.date_range(start='2023-01-01', periods=n_rows, freq='D')

    # Generate gaussian distributed data
    data = np.random.normal(0, 1, size=(n_rows, n_columns))

    # Create dataframe with date index and I columns
    df = pd.DataFrame(data, index=date_index, columns=[f'Col_{i + 1}' for i in range(n_columns)])

    return df


# Example usage: create a DataFrame with 10 rows and 3 columns
df_example = generate_gaussian_dataframe(10, 3)
print(df_example)


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