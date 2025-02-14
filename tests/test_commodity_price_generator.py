import pandas as pd
import pytest

from ctmds.commodity_price_generator import CommodityPriceGenerator
from ctmds.enums import Commodity
from ctmds.enums import CountryCode
from ctmds.enums import Granularity


@pytest.fixture
def setup():
    return {
        "for_date": "2024-03-20",
        "country_code": CountryCode.GB,
        "granularity": Granularity.HOURLY,
        "seed": 42,
    }


def test_generate_crude_price_series(setup):
    generator = CommodityPriceGenerator(Commodity.CRUDE)
    price_series = generator.generate_price_series(**setup)

    assert isinstance(price_series, pd.Series)
    assert len(price_series) == 24
    assert price_series.between(70, 90).all(), (
        f"some prices are out of expected range for CRUDE: [70, 90]: {price_series}"
    )


def test_generate_natgas_price_series(setup):
    generator = CommodityPriceGenerator(Commodity.NATGAS)
    price_series = generator.generate_price_series(**setup)

    assert isinstance(price_series, pd.Series)
    assert len(price_series) == 24
    assert price_series.between(10, 40).all(), (
        f"some prices are out of expected range for NATGAS: [10, 40]: {price_series}"
    )


def test_generate_power_price_series(setup):
    generator = CommodityPriceGenerator(Commodity.POWER)
    price_series = generator.generate_price_series(**setup)

    assert isinstance(price_series, pd.Series)
    assert len(price_series) == 24
    assert price_series.between(50, 80).all(), (
        f"some prices are out of expected range for POWER: [50, 80]: {price_series}"
    )


def test_unsupported_commodity():
    with pytest.raises(KeyError, match="UNSUPPORTED_COMMODITY"):
        CommodityPriceGenerator("UNSUPPORTED_COMMODITY")
