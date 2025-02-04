from ctmds1.random_prices import randu_prices


def test_length():
    assert len(randu_prices(5)) == 5


def test_range():
    prices = randu_prices(1000)
    assert all(0 <= price <= 100 for price in prices)


def test_precision():
    prices = randu_prices(10)
    assert all(
        isinstance(price, float) and round(price, 2) == price for price in prices
    )
