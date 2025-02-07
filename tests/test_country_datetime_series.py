import pytest

from ctmds.country_datetime_series import get_country_datetime_series


@pytest.mark.parametrize(
    "country, timezone_str",
    [
        ("GB", "Europe/London"),
        ("FR", "Europe/Paris"),
        ("NL", "Europe/Amsterdam"),
        ("DE", "Europe/Berlin"),
    ],
)
def test_standard_day(country, timezone_str):
    """Test a normal 24-hour day without DST transitions."""
    date_str = "2024-03-20"  # A day with no DST changes
    dt_series = get_country_datetime_series(date_str, country, granularity="hourly")

    assert len(dt_series) == 24, "A standard day should have 24 hours"
    assert dt_series[0].tz.zone == timezone_str, "Timezone should match expected"


@pytest.mark.parametrize(
    "country, spring_date",
    [
        ("GB", "2024-03-31"),
        ("FR", "2024-03-31"),
        ("NL", "2024-03-31"),
        ("DE", "2024-03-31"),
    ],
)
def test_spring_forward(country, spring_date):
    """Test spring forward day where one hour is skipped."""
    dt_series = get_country_datetime_series(spring_date, country, granularity="hourly")

    assert len(dt_series) == 23, "Spring forward day should have 23 hours"
    assert all(dt_series.hour[i] != dt_series.hour[i - 1] for i in range(1, len(dt_series))), (
        "No duplicate hours"
    )


@pytest.mark.parametrize(
    "country, fall_date",
    [
        ("GB", "2024-10-27"),
        ("FR", "2024-10-27"),
        ("NL", "2024-10-27"),
        ("DE", "2024-10-27"),
    ],
)
def test_fall_back(country, fall_date):
    """Test fall back day where one hour is repeated."""
    dt_series = get_country_datetime_series(fall_date, country, granularity="hourly")

    assert len(dt_series) == 25, "Fall back day should have 25 hours"
    assert any(dt_series.hour[i] == dt_series.hour[i - 1] for i in range(1, len(dt_series))), (
        "Should contain duplicate hour"
    )


@pytest.mark.parametrize(
    "granularity, expected_count",
    [
        ("hourly", 24),
        ("half-hourly", 48),
    ],
)
def test_granularity(granularity, expected_count):
    """Test different granularities (hourly vs half-hourly)."""
    dt_series = get_country_datetime_series("2024-03-20", "GB", granularity=granularity)
    assert len(dt_series) == expected_count, (
        f"Expected {expected_count} timestamps for {granularity} granularity"
    )


def test_invalid_country():
    """Test an unsupported country code."""
    with pytest.raises(ValueError, match="Unsupported country ISO code."):
        get_country_datetime_series("2024-03-20", "US")  # US is not in the mapping
