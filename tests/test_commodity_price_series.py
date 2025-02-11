import numpy as np
import pandas as pd
import pytest

from ctmds.commodity_price_series import get_commodity_price_series


# Test cases
@pytest.mark.parametrize("country_code", ["GB", "FR", "NL", "DE"])
@pytest.mark.parametrize("granularity", ["hourly", "half-hourly"])
def test_get_commodity_price_series_valid_inputs(country_code, granularity):
    """Test function with valid country codes and granularity levels."""
    df = get_commodity_price_series("2025-01-01", country_code, granularity)

    # Ensure the result is a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Ensure the DataFrame has the correct columns
    assert list(df.columns) == ["power", "natgas", "crude"]

    # Ensure the DataFrame has a DatetimeIndex
    assert isinstance(df.index, pd.DatetimeIndex)

    # Ensure the DataFrame is not empty
    assert not df.empty

    # Ensure correct time granularity
    expected_freq = "h" if granularity == "hourly" else "30min"
    assert pd.infer_freq(df.index) == expected_freq


def test_get_commodity_price_series_deterministic_with_seed():
    """Test that function returns identical results when using the same seed."""
    df1 = get_commodity_price_series("2025-01-01", "GB", "hourly", seed=42)
    df2 = get_commodity_price_series("2025-01-01", "GB", "hourly", seed=42)

    # Ensure all values are identical
    pd.testing.assert_frame_equal(df1, df2)


def test_get_commodity_price_series_different_seeds():
    """Test that different seeds produce different results."""
    df1 = get_commodity_price_series("2025-01-01", "GB", "hourly", seed=42)
    df2 = get_commodity_price_series("2025-01-01", "GB", "hourly", seed=99)

    # Ensure that at least some values are different
    assert not df1.equals(df2)


def test_get_commodity_price_series_invalid_country():
    """Test function raises an error for invalid country codes."""
    with pytest.raises(ValueError, match="Unsupported country ISO code."):
        get_commodity_price_series("2025-01-01", "XYZ")


def test_get_commodity_price_series_output_ranges():
    """Test that the price ranges are within a reasonable range."""
    df = get_commodity_price_series("2025-01-01", "GB", "hourly", seed=42)

    # Power price should generally be within 40 to 80 €/MWh
    assert df["power"].between(40, 80).all()

    # Natgas price should generally be within 10 to 40 €/MWh
    assert df["natgas"].between(10, 40).all()

    # Crude price should generally be within 70 to 90 $/barrel
    assert df["crude"].between(70, 90).all()


def test_get_commodity_price_series_correct_length():
    """Test that the number of rows matches expected frequency."""
    df_hourly = get_commodity_price_series("2025-01-01", "GB", "hourly")
    df_half_hourly = get_commodity_price_series("2025-01-01", "GB", "half-hourly")

    # Expecting 24 data points for hourly
    assert len(df_hourly) == 24

    # Expecting 48 data points for half-hourly
    assert len(df_half_hourly) == 48
