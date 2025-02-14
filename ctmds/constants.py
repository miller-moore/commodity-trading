from ctmds.enums import Commodity
from ctmds.enums import CountryCode
from ctmds.enums import Granularity


COMMODITY_BASE_PRICES = {
    # Country-specific base prices (in €/MWh for power & gas, $/barrel for crude)
    CountryCode.GB: {Commodity.POWER: 55, Commodity.NATGAS: 25, Commodity.CRUDE: 72},
    CountryCode.FR: {Commodity.POWER: 50, Commodity.NATGAS: 20, Commodity.CRUDE: 70},
    CountryCode.NL: {Commodity.POWER: 48, Commodity.NATGAS: 18, Commodity.CRUDE: 69},
    CountryCode.DE: {Commodity.POWER: 45, Commodity.NATGAS: 22, Commodity.CRUDE: 68},
}


COUNTRY_ISO_TO_TIMEZONE = {
    CountryCode.GB: "Europe/London",
    CountryCode.FR: "Europe/Paris",
    CountryCode.NL: "Europe/Amsterdam",
    CountryCode.DE: "Europe/Berlin",
}


GRANULARITY_TO_PANDAS_FREQ = {Granularity.HOURLY: "h", Granularity.HALF_HOURLY: "30min"}
