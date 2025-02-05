# ctmds

The workings up to professional grade commodity trading software tools.

## Installation

To install the project and its dependencies, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

## Usage

### CLI

You can use the CLI to generate random prices. The CLI is built using [Typer](https://typer.tiangolo.com/).

To generate \<num\> random uniform prices, run the following command:

```sh
poetry run python -m ctmds.cli generate-randu-prices <num>
```

Replace `<num>` with the number of random prices you want to generate.


To generate random normal prices for a given date and country, run the following command:

```sh
poetry run python -m ctmds.cli generate-date-country-prices <for_date> <country_code>
```

### Example

```sh
poetry run python -m ctmds.cli generate-randu-prices 10
```

This command will generate and print 10 random prices from a uniform distribution.

## Development

### Running Tests

To run the tests, use the following command:

```sh
poetry run pytest
```

