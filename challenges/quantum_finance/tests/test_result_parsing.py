import numpy as np
import pandas as pd
import numpy.testing as npt
from results_parsing import get_binary_portfolio, get_portfolio_metrics


def test_parsing():
    assets = ["a", "b", "c", "d", "e"]
    ordered_bitstring = "01010"

    expected = {
        "a": "0",
        "b": "1",
        "c": "0",
        "d": "1",
        "e": "0"
    }
    assert get_binary_portfolio(assets, ordered_bitstring) == expected


def test_portfolio_metrics():
    """Ensure the portfolio metrics return desired value"""

    #let's assume a constant .1% daily returns over the course fo 100 days
    const_returns = 1.001
    dataset = pd.DataFrame({
        'a': [np.log(const_returns)] * 100
    }
    )

    portfolio = {"a": 1}

    actual = get_portfolio_metrics(portfolio, dataset)

    # expected returns is 1.001 to the 252 power

    expected = np.power(const_returns, 252)
    npt.assert_almost_equal(actual["Returns"], expected)