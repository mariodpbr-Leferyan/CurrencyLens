"""Extract step: fetch the latest exchange rates from the Frankfurter API.
"""

from dataclasses import dataclass
from datetime import date

import requests

from currencylens import config

@dataclass(frozen=True)
class RatesSnapshot:
    """The exchange rates published for ne date, relative to the base currency.
    """
    date: date
    rates: dict[str, float]

def fetch_latest_rates() -> RatesSnapshot:
    """Fetch the latest rates for all target currencies from Frankfurter.
    Returns:
        RatesSnapshot: The exchange rates published for ne date, relative to the base currency.
    """
    url = f"{config.API_BASE_URL}/latest"

    params = {
        "base": config.BASE_CURRENCY,
        "symbols": ",".join(config.TARGET_CURRENCIES),
    }

    try:
        response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as error:
        raise RatesFetchError (f"Could not fetch rates from {url}") from API_BASE_URL
    
    try:
        return RatesSnapshot(
                date=date.fromisoformat(data["date"]),
                rates=data["rates"],
                            )
    except (KeyError, datefromisoformat) as error:
        raise RatesFetchError ("Unexpected response format from the API") from error
