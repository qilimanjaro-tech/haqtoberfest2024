import numpy as np
import pandas as pd
import yfinance
from model_params import (
    LAMBDA_1,
    LAMBDA_2,
    LAMBDA_3,
    NLAYERS,
    NSHOTS,
    NUM_ASSETS,
    RISK_FREE_RATE,
    SIGMA_TARGET,
    TOLERANCE,
    TWO_QUBIT_GATES,
    K,
    N,
)


def fetch_log_returns(start: str,end: str, tickers: str = '^GSPC ^FTSE ^N225 ^GDAXI ^IBEX') -> pd.DataFrame:
    """Downloads daily price data from Yahoo finance for five different stock indeces. Picks the closing daily price, keeps only bussiness days, fills the blank days with the previous value, computes the log returns and drops NaNs, if any. 

    Args:
        start (str): starting data in format YYYY-MM-DD
        end (str): ending data in format YYYY-MM-DD

    Returns:
        pd.DataFrame: each column must correspond to the log daily returns of each asset. 
    """
    return

def string_to_int_list(s: str) -> list[int]:
    """Converts a string of integers to a list of integers

    Args:
        s (str): bit string

    Returns:
        list[int]: list of integers
    """
    return 

def granularity(k: int = K) -> float:
    """Returns the amount of discretization depending on the number of qubits assigned per asset. This is closely related to how much can the Hamiltonian formulation be. 

    Args:
        k (int, optional): qubits per asset. Defaults to K.

    Returns:
        float: granularity
    """
    return