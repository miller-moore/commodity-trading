import time

import typer

from ctmds.commodity_price_generator import CommodityPriceGenerator
from ctmds.commodity_price_generator import get_commodity_price_series
from ctmds.country_datetime_series import get_country_datetime_series
from ctmds.enums import Commodity
from ctmds.enums import CountryCode
from ctmds.enums import Granularity
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
    country_code: CountryCode,
    granularity: Granularity = Granularity.HOURLY,
):
    """
    Generate and print prices drawn from a random normal distribution for a given date and country
    at hourly or half-hourly intervals.

    for_date : str
        The date for which to generate prices
    country_code : CountryCode
        Country code
    granularity : Granularity
        Granularity of time
    """
    BASE_PRICES = {"GB": 61, "FR": 58, "NL": 52, "DE": 57}

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
    country_code: CountryCode,
    commodity: Commodity,
    granularity: Granularity = Granularity.HOURLY,
):
    """
    Generate synthetic price series for power, natural gas, and crude oil.

    Parameters
    ----------
    for_date : str
        Date in 'YYYY-MM-DD' format.
    country_code : CountryCode
        Country code
    commodity : Commodity
        Commodity type
    granularity : Granularity, optional
        Granularity of time. Default is 'hourly'.
    """
    start = time.time()
    comm_price_generator = CommodityPriceGenerator(commodity)
    price_series = comm_price_generator.generate_price_series(for_date, country_code, granularity)
    end = time.time()
    print(
        f"Runtime of `CommodityPriceGenerator.generate_price_series`: {(end - start):.2f} seconds"
    )

    for ts, value in price_series.items():
        time_label = ts.strftime("%Y-%m-%d %H:%M")
        print(f"{time_label}: {round(value, 2)}")


if __name__ == "__main__":
    app()
