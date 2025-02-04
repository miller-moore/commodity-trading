import numpy as np
from numpy.typing import NDArray


def randu_prices(num: int, decimals: int = 2) -> NDArray[np.float64]:
    """Generate an array of random prices from a uniform distribution.

    num : int
        The number of random prices to generate.
    """
    return np.round(np.random.uniform(0, 100, num), decimals)
