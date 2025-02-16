from enum import Enum


class CountryCode(str, Enum):
    GB = "GB"
    FR = "FR"
    NL = "NL"
    DE = "DE"

    def to_timezone_str(self) -> str:
        from ctmds.constants import COUNTRY_ISO_TO_TIMEZONE

        if self not in COUNTRY_ISO_TO_TIMEZONE:
            raise ValueError(
                f"timezone not defined for {self}, known country timezones: "
                f"{COUNTRY_ISO_TO_TIMEZONE}"
            )
        return COUNTRY_ISO_TO_TIMEZONE[self]


class Granularity(str, Enum):
    HOURLY = "HOURLY"
    HALF_HOURLY = "HALF_HOURLY"

    def to_pandas_freq(self) -> str:
        from ctmds.constants import GRANULARITY_TO_PANDAS_FREQ

        if self not in GRANULARITY_TO_PANDAS_FREQ:
            raise ValueError(
                f"pandas freq not defined for {self}, known pandas frequencies: "
                f"{GRANULARITY_TO_PANDAS_FREQ}"
            )
        return GRANULARITY_TO_PANDAS_FREQ[self]


class Commodity(str, Enum):
    NATGAS = "NATGAS"
    POWER = "POWER"
    CRUDE = "CRUDE"
