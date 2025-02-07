import numpy as np
from numpy.typing import NDArray


RNG = np.random.default_rng()  # Create a Generator instance


def rand_uniform_prices(num: int, decimals: int = 2) -> NDArray[np.float64]:
    """
    Generate an array of random prices from a uniform distribution.

    num : int
        The number of random prices to generate
    decimals : int
        Number of decimals for rounding precision
    """
    return np.round(RNG.uniform(0, 100, num), decimals)


def rand_normal_prices(
    loc: float, scale: float, num: int, decimals: int = 2
) -> NDArray[np.float64]:
    """
    Generate an array of random prices from a uniform distribution.

    loc : float
        Mean of the distribution.
    scale : float
        Standard deviation (spread or "width") of the distribution. Must be non-negative.
    num : int
        The number of random prices to generate
    decimals : int
        Number of decimals for rounding precision
    """
    return np.round(RNG.normal(loc, scale, num), decimals)
