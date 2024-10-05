import pytest
import pandas as pd
import numpy as np

from challenge.model_params import NUM_ASSETS, K

@pytest.fixture
def dataset():

    def generate_gaussian_dataframe(n_rows: int, n_columns: int):
        # Create date range for index
        date_index = pd.date_range(start='2023-01-01', periods=n_rows, freq='D')

        # Generate gaussian distributed data
        data = np.random.normal(0, 1, size=(n_rows, n_columns))

        # Create dataframe with date index and I columns
        df = pd.DataFrame(data, index=date_index, columns=[f'Asset_{i + 1}' for i in range(n_columns)])

        return df

    # Example usage: create a DataFrame with 10 rows and 3 columns
    return generate_gaussian_dataframe(10, NUM_ASSETS)

@pytest.fixture
def bitstring():
    return np.random.choice([1, -1], size=NUM_ASSETS * K)