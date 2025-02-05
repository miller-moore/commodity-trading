import datetime
import time

import typer

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
def generate_date_country_prices(
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
    num_intervals = 24 if granularity == "hourly" else 48
    interval_minutes = 60 if granularity == "hourly" else 30

    start = time.time()
    prices = rand_normal_prices(base_price, scale=1, num=num_intervals, decimals=2)
    end = time.time()
    print(f"Runtime of {num_intervals} `rand_normal_prices`: {(end - start):.2f} seconds")

    start_time = datetime.datetime.strptime(for_date, "%Y-%m-%d")
    for i in range(num_intervals):
        time_label = (start_time + datetime.timedelta(minutes=i * interval_minutes)).strftime(
            "%Y-%m-%d %H:%M"
        )
        print(f"{time_label}: {prices[i]:,.2f}")


if __name__ == "__main__":
    app()
