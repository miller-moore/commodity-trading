from ctmds.random_prices import rand_normal_prices
from ctmds.random_prices import rand_uniform_prices


def test_rand_uniform_prices_length():
    assert len(rand_uniform_prices(5)) == 5


def test_rand_uniform_prices_range():
    prices = rand_uniform_prices(1000)
    assert all(0 <= price <= 100 for price in prices)


def test_rand_uniform_prices_precision():
    prices = rand_uniform_prices(10)
    assert all(isinstance(price, float) and round(price, 2) == price for price in prices)


def test_rand_normal_prices_length():
    loc = 0
    scale = 1
    num = 10
    prices = rand_normal_prices(loc, scale, num)
    assert len(prices) == num


def test_rand_normal_prices_precision():
    loc = 0
    scale = 1
    num = 10
    decimals = 3
    prices = rand_normal_prices(loc, scale, num, decimals)
    assert all(isinstance(price, float) and round(price, decimals) == price for price in prices)
