import time

import typer

from ctmds.commodity_price_series import get_commodity_price_series
from ctmds.country_datetime_series import get_country_datetime_series
from ctmds.random_prices import rand_normal_prices
from ctmds.random_prices import rand_uniform_prices


app = typer.Typer()


@app.command()
def generate_randu_prices(num: int):
    """
    Generate and print random prices from a uniform distribution.

    num : int
        The number of random prices to generate.
    """
    start = time.time()
    prices = rand_uniform_prices(num)
    end = time.time()

    print(f"Runtime of {num} `randu_prices`: {(end - start):.2f} seconds")
    print(prices)


@app.command()
def generate_country_datetime_prices(
    for_date: str,
    country_code: str,
    granularity: str = "hourly",
):
    """
    Generate and print prices drawn from a random normal distribution for a given date and country
    at hourly or half-hourly intervals.

    for_date : str
        The date for which to generate prices
    country_code : str
        Country code from the accepted list of options, must be in ["GB", "FR", "NL", "DE"]
    granularity : str
        Granularity of time at which to generate prices, must be in ["hourly", "half-hourly"]
    """
    BASE_PRICES = {"GB": 61, "FR": 58, "NL": 52, "DE": 57}

    if country_code not in BASE_PRICES:
        raise ValueError(f"Unsupported country code, must be in {list(BASE_PRICES)}")

    if granularity not in ["hourly", "half-hourly"]:
        raise ValueError(f"Unsupported granularity, must be in {['hourly', 'half-hourly']}")

    base_price = BASE_PRICES[country_code]
    timeseries = get_country_datetime_series(for_date, country_code, granularity)
    num = len(timeseries)

    start = time.time()
    prices = rand_normal_prices(base_price, scale=1, num=num, decimals=2)
    end = time.time()
    print(f"Runtime of {num} `rand_normal_prices`: {(end - start):.2f} seconds")

    for i, ts in enumerate(timeseries):
        time_label = ts.strftime("%Y-%m-%d %H:%M")
        print(f"{time_label}: {prices[i]:,.2f}")


@app.command()
def generate_commodity_datetime_prices(
    for_date: str,
    country_code: str,
    commodity: str,
    granularity: str = "hourly",
):
    """
    Generate synthetic price series for power, natural gas, and crude oil.

    Parameters
    ----------
    for_date : str
        Date in 'YYYY-MM-DD' format.
    country_code : str
        One of ['GB', 'FR', 'NL', 'DE'] representing the country code.
    commodity : str
        One of ['natgas','power','crude'] representing the commodity type.
    granularity : str, optional
        Frequency of data points, one of ['hourly', 'half-hourly']. Default is 'hourly'.
    """
    COUNTRY_CODES = ["GB", "FR", "NL", "DE"]

    if country_code not in COUNTRY_CODES:
        raise ValueError(f"Unsupported country code, must be in {COUNTRY_CODES}")

    COMMODITIES = ["natgas", "power", "crude"]
    if commodity not in COMMODITIES:
        raise ValueError(f"Unsupported commodity, must be in {COMMODITIES}")

    if granularity not in ["hourly", "half-hourly"]:
        raise ValueError(f"Unsupported granularity, must be in {['hourly', 'half-hourly']}")

    start = time.time()
    df_prices = get_commodity_price_series(for_date, country_code, granularity)
    end = time.time()
    print(f"Runtime of `get_commodity_price_series`: {(end - start):.2f} seconds")

    for ts, row in df_prices.iterrows():
        time_label = ts.strftime("%Y-%m-%d %H:%M")
        print(f"{time_label}: {row[commodity].round(2)}")


if __name__ == "__main__":
    app()
