import numpy as np
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
    """Returns the minimum energy of a portfolio

    Args:
        portfolios (dict): _description_

    Returns:
        float: _description_
    """

    min_energy = float('inf')
    for _, metrics in portfolios.items():
        energy = metrics.get('energy')
        if energy is not None and energy < min_energy:
            min_energy = energy

    return min_energy

def get_max_prob(result: CircuitResult, nshots: int = NSHOTS) -> float:
    """Returns the maximum probability amongst all the portfolios

    Args:
        result (CircuitResult): _description_
        nshots (int, optional): _description_. Defaults to NSHOTS.

    Returns:
        float: max prob
    """
    frequencies = result.frequencies().values()
    
    max_prob = 0
    for freq in frequencies:
        if (prob := freq / nshots) > max_prob:
            max_prob = prob

    return max_prob

def get_optimal_binary_portfolios_prob_and_energy(ansatz: Circuit, dataset: pd.DataFrame, nshots: int = NSHOTS, tolerance: int = TOLERANCE) -> dict:
    """Returns the portfolios that turned out to have a certain probability. The threshold is defined as `1-docstring_probability < TOLERANCE`. 
    
    It is suggested to call get_max_prob() and compute_cost_function().

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
    max_prob = get_max_prob(result, nshots)
    
    for bit_string, stat_freq in result.frequencies().items():
        prob = stat_freq / nshots
        if (max_prob - prob) < tolerance:
            optimal_portfolios[bit_string] = {
                'stat_freq': prob, 'energy': compute_cost_function(dataset, string_to_int_list(bit_string))}
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
    binary_portfolio = {}
    for i in range(len(assets)):
        binary_portfolio[assets[i]] = ordered_bitstring[i*num_qubit_per_asset:(i+1)*num_qubit_per_asset]
    return binary_portfolio

def get_asset_weight_decimal(asset_bit_string: str) -> float:
    """Given a bistring that represent the weight of one asset, translates it to the decimal base.

    Args:
        asset_bit_string (_type_): bitstring

    Returns:
        _type_: _description_
    """
    return int(asset_bit_string, 2) / (2 ** len(asset_bit_string))

def get_decimal_portfolio(binary_portfolio: dict) -> dict:
    """Given a binary portfolio, it returns the corresponding portfolio in the decimal base
    Defining and calling get_asset_weight_decimal(asset_bit_string: str) -> float may be of help.  

    Args:
        binary_portfolio (_type_): _description_

    Returns:
        dict: e.g {'asset1':0.23, 'asset2':0.4 ...}
    """
    decimal_portfolio = {}
    for asset, bit_string in binary_portfolio.items():
        decimal_portfolio[asset] = get_asset_weight_decimal(bit_string)
    return decimal_portfolio
        
def get_portfolio_metrics(portfolio: dict, dataset: pd.DataFrame, r: float = RISK_FREE_RATE) -> dict:
    """Calculates the anualized return, volatilty and Sharp Ratio. Assume log returns are normally distributed.

    Args:
        portfolio (dict): decimal portfolio
        dataset (pd.DataFrame): _description_
        r (float, optional): _description_. Defaults to RISK_FREE_RATE.

    Returns:
        _type_: _description_
    """
    assets = list(portfolio.keys())
    # Calculate mean returns for each asset
    mean_returns = dataset[list(portfolio.keys())].mean()

    # Calculate the weighted sum of returns
    portfolio_return = sum(portfolio[asset] * mean_returns[asset] for asset in portfolio)

    # Calculate annualized return (assuming 252 trading days in a year)
    annualized_return = (1 + portfolio_return) ** 252 - 1

    weights_array = np.array([portfolio[asset] for asset in assets])
    cov_matrix = dataset[assets].cov()
    # Calculate portfolio variance
    portfolio_variance = weights_array.T @ cov_matrix @ weights_array

    # Calculate annualized volatility (assuming daily returns and 252 trading days)
    annualized_volatility = np.sqrt(portfolio_variance) * np.sqrt(252)

    sharpe_ratio = (annualized_return - r) / annualized_volatility

    return {'Returns': annualized_return,
    'Volatility': annualized_volatility,
    'Sharpe Ratio': sharpe_ratio,
    'Normalized Weights': weights_array}