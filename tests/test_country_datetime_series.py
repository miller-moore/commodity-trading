import pytest

from ctmds.country_datetime_series import get_country_datetime_series
from ctmds.enums import CountryCode
from ctmds.enums import Granularity


@pytest.mark.parametrize("country_code", list(CountryCode))
def test_standard_day(country_code):
    """Test a normal 24-hour day without DST transitions."""
    date_str = "2024-03-20"  # A day with no DST changes
    dt_series = get_country_datetime_series(date_str, country_code, granularity=Granularity.HOURLY)

    assert len(dt_series) == 24, "A standard day should have 24 hours"
    assert dt_series[0].tz.zone == country_code.to_timezone_str(), "Timezone should match expected"


@pytest.mark.parametrize(
    "country_code, spring_date",
    list(zip(list(CountryCode), ["2024-03-31", "2024-03-31", "2024-03-31", "2024-03-31"])),
)
def test_spring_forward(country_code, spring_date):
    """Test spring forward day where one hour is skipped."""
    dt_series = get_country_datetime_series(
        spring_date, country_code, granularity=Granularity.HOURLY
    )

    assert len(dt_series) == 23, "Spring forward day should have 23 hours"
    assert all(dt_series.hour[i] != dt_series.hour[i - 1] for i in range(1, len(dt_series))), (
        "No duplicate hours"
    )


@pytest.mark.parametrize(
    "country_code, fall_date",
    list(zip(list(CountryCode), ["2024-10-27", "2024-10-27", "2024-10-27", "2024-10-27"])),
)
def test_fall_back(country_code, fall_date):
    """Test fall back day where one hour is repeated."""
    dt_series = get_country_datetime_series(fall_date, country_code, granularity=Granularity.HOURLY)

    assert len(dt_series) == 25, "Fall back day should have 25 hours"
    assert any(dt_series.hour[i] == dt_series.hour[i - 1] for i in range(1, len(dt_series))), (
        "Should contain duplicate hour"
    )


@pytest.mark.parametrize(
    "granularity, expected_count",
    [
        (Granularity.HOURLY, 24),
        (Granularity.HALF_HOURLY, 48),
    ],
)
def test_granularity(granularity, expected_count):
    """Test different granularities (hourly vs half-hourly)."""
    dt_series = get_country_datetime_series("2024-03-20", CountryCode.GB, granularity=granularity)
    assert len(dt_series) == expected_count, (
        f"Expected {expected_count} timestamps for {granularity} granularity"
    )


def test_invalid_country():
    """Test an unsupported country code."""
    with pytest.raises(KeyError, match="UNSUPPORTED_COUNTRY_CODE"):
        get_country_datetime_series(
            "2024-03-20", "UNSUPPORTED_COUNTRY_CODE", granularity=Granularity.HOURLY
        )
