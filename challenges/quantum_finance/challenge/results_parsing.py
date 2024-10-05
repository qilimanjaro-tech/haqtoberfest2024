from typing import Tuple

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
    """Returns the minimum energy of a portfolio.

    Args:
        portfolios (dict): all the considered porfolios (sets
            of weigths for the assets). THese are the ones obtained
            in the measurement.

    Returns:
        float: energy of the minimum energy portfolio
        dict: the portfolio that gives the minimum energy.
    """

    min_energy = float('inf')
    min_energy_portfolio = "none"
    for k, metrics in portfolios.items():
        energy = metrics.get('energy')
        if energy is not None and energy < min_energy:
            min_energy = energy
            min_energy_portfolio = k

    return min_energy, min_energy_portfolio


def get_max_prob(result: CircuitResult, nshots: int = NSHOTS) -> float:
    """Returns the maximum probability among all the portfolios,
    the one that most appeared among the Qcircuit runs.

    Args:
        result (CircuitResult): result of the circuit run.
        nshots (int, optional): number of times we have runned the circuit.
            Defaults to NSHOTS.

    Returns:
        float: max probability
    """
    # Get all the frequencies (how many times we have each portfolio)
    frequencies = result.frequencies().values()

    max_prob = 0
    for freq in frequencies:
        if (prob := freq / nshots) > max_prob:
            max_prob = prob

    return max_prob


def get_optimal_binary_portfolios_prob_and_energy(ansatz: Circuit, dataset: pd.DataFrame, nshots: int = NSHOTS,
                                                  tolerance: int = TOLERANCE) -> dict:
    """Returns the portfolios that turned out to have a certain probability.
    The threshold is defined as `1-docstring_probability < TOLERANCE`. 

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
                'stat_freq': prob,
                'energy': compute_cost_function(dataset,
                                                string_to_int_list(bit_string))}
    return optimal_portfolios


def get_binary_portfolio(assets: list, ordered_bitstring, num_qubit_per_asset=K) -> dict:
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
        binary_portfolio[assets[i]] = ordered_bitstring[i * num_qubit_per_asset:(i + 1) * num_qubit_per_asset]
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
    annualized_return = portfolio_return * 252

    weights_array = np.array([portfolio[asset] for asset in assets])
    cov_matrix = dataset[assets].cov()
    # Calculate portfolio variance
    portfolio_variance = weights_array.T @ cov_matrix @ weights_array

    # Calculate annualized volatility (assuming daily returns and 252 trading days)
    annualized_volatility = np.sqrt(portfolio_variance) * np.sqrt(252)

    sharpe_ratio = (annualized_return - r) / annualized_volatility

    return {'Returns': np.exp(annualized_return),
            'Volatility': annualized_volatility,
            'Sharpe Ratio': sharpe_ratio,
            'Normalized Weights': weights_array}
