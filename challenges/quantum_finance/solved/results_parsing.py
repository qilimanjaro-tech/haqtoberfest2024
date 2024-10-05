import pandas as pd
from cost_function import compute_cost_function
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
from qibo.models import Circuit
from qibo.result import CircuitResult
from utils import string_to_int_list


def get_minimum_energy(portfolios: dict) -> float:
    energies = []
    for data in portfolios.values():
        energies.append(data['energy'])
    return min(energies)

def get_max_prob(result: CircuitResult, nshots: int = NSHOTS) -> float:
    number_of_times = result.frequencies().values()
    probs = [freq/nshots for freq in number_of_times]
    return max(probs)

def get_optimal_binary_portfolios_prob_and_energy(ansatz: Circuit, dataset: pd.DataFrame, nshots: int = NSHOTS, tolerance: int = TOLERANCE) -> dict:
    """Returns the portfolios that turned out to have a certain probability. The threshold is defined as `1-docstring_probability < TOLERANCE`. It is suggested to call get_max_prob() and compute_cost_function().

    Args:
        ansatz (Circuit): _description_
        dataset (pd.DataFrame): _description_
        nshots (int, optional): _description_. Defaults to NSHOTS.
        tolerance (int, optional): _description_. Defaults to TOLERANCE.

    Returns:
        dict: _description_
    """
    result = ansatz(nshots=nshots)
    optimal_portfolios = {}
    for bit_string, stat_freq in result.frequencies().items():
        if (get_max_prob(result) - stat_freq/nshots) < tolerance:
            optimal_portfolios[bit_string] = {'stat_freq': stat_freq/nshots, 'energy': compute_cost_function(dataset, string_to_int_list(bit_string))}
    return optimal_portfolios

def get_binary_portfolio(assets: list, ordered_bitstring, num_qubit_per_asset = K) -> dict:
    """Returns a binry portfolio -e.g, {'asset_1':'110, 'asset_2':'101'}. To provide the assets you can user DataFrame.columns.

    Args:
        assets (_type_): name of the asset
        ordered_bitstring (_type_): portfolio
        num_qubit_per_asset (_type_, optional): _description_. Defaults to K.

    Returns:
        dict: binary portfolio
    """
    weights = [ordered_bitstring[i:i+num_qubit_per_asset] for i in range(0, len(ordered_bitstring),num_qubit_per_asset)]
    return dict(zip(assets,weights))

def get_asset_weight_decimal(asset_bit_string: str) -> float:
    """Given a bistring that represent the weight of one asset, translates it to the decimal base.

    Args:
        asset_bit_string (_type_): bitstring

    Returns:
        _type_: _description_
    """
    w = 0
    for k,bit in enumerate(asset_bit_string):
       w += 2**(k-1)*int(bit)*1/(2**len(asset_bit_string)) # discretization !
    return w  

def get_decimal_portfolio(binary_portfolio: dict) -> dict:
    """Given a binary portfolio, it returns the corresponding portfolio in the decimal base
    Defining and calling get_asset_weight_decimal(asset_bit_string: str) -> float may be of help.  

    Args:
        binary_portfolio (_type_): _description_

    Returns:
        dict: e.g {'asset1':0.23, 'asset2':0.4 ...}
    """
    portfolio = {}
    for asset, w in binary_portfolio.items():
        portfolio[asset] = get_asset_weight_decimal(w)
    return portfolio
        
def get_portfolio_metrics(portfolio: dict, dataset: pd.DataFrame, r: float = RISK_FREE_RATE) -> dict:
    """Calculates the anualized return, volatilty and Sharp Ratio. Assume log returns are normally distributed.

    Args:
        portfolio (dict): decimal portfolio
        dataset (pd.DataFrame): _description_
        r (float, optional): _description_. Defaults to RISK_FREE_RATE.

    Returns:
        _type_: _description_
    """
    import numpy as np
    normalized_weights = list(portfolio.values()) / np.sum(list(portfolio.values()))


    # Calculate the expected log returns, and add them to the `returns_array`.
    annualized_ret_portfolio = np.sum((dataset.mean() * normalized_weights) * 252)


    # Calculate the volatility, and add them to the `volatility_array`.
    annualized_vol_portfolio = np.sqrt(
        np.dot(normalized_weights.T, np.dot(dataset.cov() * 252, normalized_weights))
    )
    annualized_ret_portfolio,annualized_vol_portfolio

    # Calculate the Sharpe Ratio and Add it to the `sharpe_ratio_array`.
    sharpe_ratio= (annualized_ret_portfolio-r)/annualized_vol_portfolio

    # Let's create our "Master Data Frame", with the weights, the returns, the volatility, and the Sharpe Ratio
    return {'Returns':annualized_ret_portfolio, 'Volatility':annualized_vol_portfolio, 'Sharpe Ratio':sharpe_ratio, 'Normalized Weights':normalized_weights}