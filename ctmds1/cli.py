import click

from ctmds1.random_prices import randu_prices


@click.command()
@click.argument("num", type=int)
def generate_randu_prices(num: int):
    """Generate and print random prices from a uniform distribution.

    num : int
        The number of random prices to generate.
    """
    prices = randu_prices(num)
    print(prices)


if __name__ == "__main__":
    generate_randu_prices()
