from datetime import datetime
from datetime import timedelta

import pandas as pd
import pytz


COUNTRY_ISO_TO_TIMEZONE = {
    "GB": "Europe/London",
    "FR": "Europe/Paris",
    "NL": "Europe/Amsterdam",
    "DE": "Europe/Berlin",
}


def get_country_datetime_series(
    date_str: str, country_code: str, granularity: str = "hourly"
) -> pd.DatetimeIndex:
    """
    Get the point-in-time accurate timestamps for a given date and country ISO code,
    accounting for daylight savings time transitions by detecting if a given date is a daylight
    saving transition (spring forward or fall back).

    On spring forward dates, this will result in fewer timestamps than in a normal 24 hour period.
    On fall back dates, this will result in more timestamps than in a normal 24 hour period.
    """
    if country_code not in COUNTRY_ISO_TO_TIMEZONE:
        raise ValueError("Unsupported country ISO code.")

    tz = pytz.timezone(COUNTRY_ISO_TO_TIMEZONE[country_code])

    # Convert input date to a datetime object at midnight
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=0, minute=0)

    # Get the timezone naive time series
    freq = "h" if granularity == "hourly" else "30min"
    naive_range = pd.date_range(start=dt, end=dt + timedelta(days=1, seconds=-1), freq=freq)

    ## Auto-detect DST transition:
    # Localize in "strict" mode to avoid automatic DST correction
    dt_before = tz.localize(dt, is_dst=None)
    dt_after = tz.localize(dt + timedelta(days=1), is_dst=None)
    # Get UTC offset before and after transition to detect if spring forward, fall back, or neither
    offset_before = dt_before.utcoffset()
    offset_after = dt_after.utcoffset()

    # Get final timezone-aware timeseries, with proper timestamp values
    if offset_before < offset_after:
        # Spring Forward (DST Start)
        # print("spring forward")
        # Convert to timezone-aware timestamps
        aware_range = naive_range.tz_localize(tz, nonexistent="NaT")
        # Drop NaT values (times that don't exist on spring forward)
        return aware_range.dropna()
    elif offset_before > offset_after:
        # Fall Back (DST End)
        # print("fall back")
        # Combine two series, one that uses DST before transition & other uses non-DST after trans
        first_occurrence = naive_range.tz_localize(tz, ambiguous=False)
        second_occurrence = naive_range.tz_localize(tz, ambiguous=True)
        # Drop duplicates, effectively keeping the hours over the transition period
        return (
            pd.concat([first_occurrence.to_series(), second_occurrence.to_series()])
            .drop_duplicates(keep="first")
            .sort_values()
            .index
        )
    else:
        # No DST Transition
        return naive_range.tz_localize(tz)
