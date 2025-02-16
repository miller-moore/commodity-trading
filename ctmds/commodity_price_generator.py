import numpy as np
import pandas as pd

from ctmds.constants import COMMODITY_BASE_PRICES
from ctmds.country_datetime_series import get_country_datetime_series
from ctmds.enums import Commodity
from ctmds.enums import CountryCode
from ctmds.enums import Granularity


class CommodityPriceGenerator:
    def __init__(self, commodity: Commodity):
        self.commodity = Commodity[commodity]

    def generate_price_series(
        self,
        for_date: str,
        country_code: CountryCode,
        granularity: Granularity = Granularity.HOURLY,
        seed: int | None = None,
    ) -> pd.Series:
        """
        Generate synthetic price series for the commodity.

        Parameters
        ----------
        for_date : str
            Date in 'YYYY-MM-DD' format.
        country_code : CountryCode
            Country code
        granularity : Granularity, optional
            Granularity of time. Default is 'hourly'.
        seed : int | None, optional
            Seed for random number generator. Default is None

        Returns
        -------
        pd.Series
            Series of prices with pd.DatetimeIndex index
        """
        dates = get_country_datetime_series(for_date, country_code, granularity)

        PRICE_FUNCTIONS = {
            Commodity.CRUDE: generate_crude_prices,
            Commodity.NATGAS: generate_natgas_prices,
            Commodity.POWER: generate_power_prices,
        }

        prices = PRICE_FUNCTIONS[self.commodity](dates, country_code, seed)

        return pd.Series(prices, index=dates)


def generate_crude_prices(
    dates: pd.DatetimeIndex, country_code: CountryCode, seed: int | None = None
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    # Create a datetime index
    n = len(dates)
    days = dates.dayofyear

    base_price = COMMODITY_BASE_PRICES[country_code][Commodity.CRUDE]

    # Seasonal effect using sine wave
    # Annual seasonality (365.25 days cycle)
    # Peaks in January and July, troughs in April and October
    annual_cycle = 4 * np.pi * (days - 365.25 / 2) / 365.25

    # Double cosine to create two peaks and two troughs per year
    seasonal_intensity = 1 + 0.5 * np.cos(annual_cycle)

    crude_seasonality = seasonal_intensity * 5  # ±5 $/barrel

    # Random normal noise
    crude_noise = rng.normal(0, 0.75, n)  # standard deviation of 0.75 $/barrel

    # Generate price series
    prices = base_price + crude_seasonality + crude_noise

    return prices


def generate_natgas_prices(
    dates: pd.DatetimeIndex,
    country_code: CountryCode,
    seed: int | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    n = len(dates)
    hours = dates.hour
    days = dates.dayofyear

    base_price = COMMODITY_BASE_PRICES[country_code][Commodity.NATGAS]

    # Seasonal effect using sine wave
    # Annual seasonality (365.25 days cycle)
    # Peaks in January and July, troughs in April and October
    annual_cycle = 4 * np.pi * (days - 365.25 / 2) / 365.25

    # Double cosine to create two peaks and two troughs per year
    seasonal_intensity = 1 + 0.5 * np.cos(annual_cycle)

    natgas_seasonality = seasonal_intensity * 5  # ±5 €/MWh

    # Daily peak/off-peak factors
    peak_hours = (hours >= 16) & (hours <= 20)  # 4 to 8 PM as peak hours
    natgas_peak_factor = np.where(peak_hours, 2, -2)  # ±2 €/MWh variation

    # Random normal noise
    natgas_noise = rng.normal(0, 0.5, n)  # standard deviation of 0.5 €/MWh

    # Generate price series
    prices = base_price + natgas_seasonality + natgas_peak_factor + natgas_noise

    return prices


def generate_power_prices(
    dates: pd.DatetimeIndex,
    country_code: CountryCode,
    seed: int | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    n = len(dates)
    hours = dates.hour
    days = dates.dayofyear

    base_price = COMMODITY_BASE_PRICES[country_code][Commodity.POWER]

    # Seasonal effect using sine wave
    # Annual seasonality (365.25 days cycle)
    # Peaks in January and July, troughs in April and October
    annual_cycle = 4 * np.pi * (days - 365.25 / 2) / 365.25

    # Double cosine to create two peaks and two troughs per year
    seasonal_intensity = 1 + 0.5 * np.cos(annual_cycle)

    power_seasonality = seasonal_intensity * 10  # ±10 €/MWh

    # Daily peak/off-peak factors
    peak_hours = (hours >= 16) & (hours <= 20)  # 4 to 8 PM as peak hours
    power_peak_factor = np.where(peak_hours, 5, -5)  # ±5 €/MWh variation

    # Random normal noise
    power_noise = rng.normal(0, 1, n)  # standard deviation of 1 €/MWh

    # Generate price series
    prices = base_price + power_seasonality + power_peak_factor + power_noise

    return prices
