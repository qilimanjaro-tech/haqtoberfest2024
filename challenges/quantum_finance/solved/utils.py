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


def fetch_log_returns(start: str,end: str) -> pd.DataFrame:
    """Downloads daily price data from Yahoo finance for five different stock indeces. Picks the closing daily price, keeps only bussiness days, fills the blank days with the previous value, computes the log returns and drops NaNs, if any. 

    Args:
        start (str): _description_
        end (str): _description_

    Returns:
        pd.DataFrame: 
    """
    raw_data = yfinance.download(tickers = '^GSPC ^FTSE ^N225 ^GDAXI ^IBEX', 
                                start=start, end=end, interval = '1d', group_by = 'ticker',
                                auto_adjust = True)
    df_comp = pd.DataFrame(raw_data.copy())
    # pick data from the first day to the last one 
    df_comp = df_comp.iloc[1:]

    #add columns
    df_comp['sp500'] = df_comp['^GSPC'].Close[:]
    df_comp['dax'] = df_comp['^GDAXI'].Close[:]
    df_comp['ftse'] = df_comp['^FTSE'].Close[:]
    df_comp['nikkei'] = df_comp['^N225'].Close[:]
    df_comp['ibex'] = df_comp['^IBEX'].Close[:]

    #remove columns
    del df_comp['^GSPC'], df_comp['^GDAXI'], df_comp['^FTSE'], df_comp['^N225'], df_comp['^IBEX']

    price_data_frame = df_comp.asfreq('b') # only keeping bussiness days as the stock market is closed on weekends
    price_data_frame = df_comp.ffill() #forward fill
    price_data_frame = price_data_frame[1:]
    
    log_return = np.log(price_data_frame/price_data_frame.shift(1))
    log_return.columns = [c[0] for c in log_return.columns]
    return log_return.dropna()

def string_to_int_list(s: str) -> list[int]:
    """Converts a string of integers to a list of integers

    Args:
        s (str): bit string

    Returns:
        list[int]: list of integers
    """
    return [int(char) for char in s]

def granularity(k: int = K) -> float:
    """Returns the amount of discretization depending on the number of qubits assigned per asset. This is closely related to how much can the Hamiltonian formulation be. 

    Args:
        k (int, optional): qubits per asset. Defaults to K.

    Returns:
        float: granularity
    """
    return 1/(2**k)