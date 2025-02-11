import numpy as np
import pandas as pd

from ctmds.country_datetime_series import get_country_datetime_series


def get_commodity_price_series(for_date, country_code, granularity: str = "hourly", seed=None):
    """
    Generate synthetic price series for power, natural gas, and crude oil.

    Parameters
    ----------
    for_date : str
        Date in 'YYYY-MM-DD' format.
    country_code : str
        One of ['GB', 'FR', 'NL', 'DE'] representing the country code.
    granularity : str, optional
        Frequency of data points, one of ['hourly', 'half-hourly']. Default is 'hourly'.
    seed : int or None, optional
        Seed for the random number generator. Default is None.

    Returns
    -------
    DataFrame
        DataFrame with datetime index and price columns for power, natural gas, and crude oil.
    """
    # Create a datetime index
    dates = get_country_datetime_series(for_date, country_code, granularity)
    n = len(dates)
    hours = dates.hour
    days = dates.dayofyear

    # Country-specific base prices (in €/MWh for power & gas, $/barrel for crude)
    base_prices = {
        "GB": {"power": 55, "natgas": 25, "crude": 72},
        "FR": {"power": 50, "natgas": 20, "crude": 70},
        "NL": {"power": 48, "natgas": 18, "crude": 69},
        "DE": {"power": 45, "natgas": 22, "crude": 68},
    }

    # Get country-specific base prices
    base_power_price = base_prices[country_code]["power"]
    base_natgas_price = base_prices[country_code]["natgas"]
    base_crude_price = base_prices[country_code]["crude"]

    # Seasonal effect using sine wave
    # Annual seasonality (365.25 days cycle)
    # Peaks in January and July, troughs in April and October
    annual_cycle = 4 * np.pi * (days - 365.25 / 2) / 365.25

    # Double cosine to create two peaks and two troughs per year
    seasonal_intensity = 1 + 0.5 * np.cos(annual_cycle)

    power_seasonality = seasonal_intensity * 10  # ±10 €/MWh
    natgas_seasonality = seasonal_intensity * 5  # ±5 €/MWh
    crude_seasonality = seasonal_intensity * 5  # ±5 $/barrel

    # Daily peak/off-peak factors
    peak_hours = (hours >= 16) & (hours <= 20)  # 4 to 8 PM as peak hours
    power_peak_factor = np.where(peak_hours, 5, -5)  # ±5 €/MWh variation
    natgas_peak_factor = np.where(peak_hours, 2, -2)  # ±2 €/MWh variation

    # Random generator
    rng = np.random.default_rng(seed)

    # Random normal noise
    power_noise = rng.normal(0, 1, n)  # standard deviation of 1 €/MWh
    natgas_noise = rng.normal(0, 0.5, n)  # standard deviation of 0.5 €/MWh
    crude_noise = rng.normal(0, 0.75, n)  # standard deviation of 0.75 $/barrel

    # Generate price series
    power_prices = base_power_price + power_seasonality + power_peak_factor + power_noise
    natgas_prices = base_natgas_price + natgas_seasonality + natgas_peak_factor + natgas_noise
    crude_prices = base_crude_price + crude_seasonality + crude_noise

    # Create DataFrame
    df = pd.DataFrame(
        {"power": power_prices, "natgas": natgas_prices, "crude": crude_prices},
        index=dates,
    )

    return df
