"""Tests for currencylens.fetch_rates (no real network calls)."""

from datetime import date
from unittest import mock

import pytest
import requests

from currencylens.fetch_rates import RatesFetchError, RatesSnapshot, fetch_latest_rates

def make_response(json_data):
    """Build a fake request.Response that returns json_data."""
    response = mock.Mock()
    response.json.return_value = json_data
    return response


def test_fetch_latest_rates_returns_snapshot():
    fake_payload = {"date": "2026-10-07", "rates": {"AUD": 1.2221, "BRL": 5.7777, "CAD": 1.5555}}

    with mock.patch("currencylens.fetch_rates.requests.get", return_value=make_response(fake_payload)):
        snapshot = fetch_latest_rates()

    assert snapshot == RatesSnapshot(date=date(2026, 10, 7), rates=fake_payload["rates"])


def test_fetch_latest_rates_raises_on_timeout():
    
    with mock.patch("currencylens.fetch_rates.requests.get", side_effect=requests.exceptions.Timeout):
        with pytest.raises(RatesFetchError, match="Could not fetch rates"):
            fetch_latest_rates()


def test_fetch_latest_rates_raises_on_http_error():
    response = make_response({"date": "2026-10-07", "rates": {"USD": 1.1}})
    response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    
    with mock.patch("currencylens.fetch_rates.requests.get", return_value=response):
        with pytest.raises(RatesFetchError, match="Could not fetch rates"):
            fetch_latest_rates()


def test_fetch_latest_rates_raises_on_missing_date():
    fake_payload = {"rates": {"USD": 1.1}}
    
    with mock.patch("currencylens.fetch_rates.requests.get", return_value=make_response(fake_payload)):
        with pytest.raises(RatesFetchError, match="Unexpected response format"):
            fetch_latest_rates()

     
def test_fetch_latest_rates_raises_on_invalid_date():
    payload = {"date": "not-a-date", "rates": {}}
    
    with mock.patch("currencylens.fetch_rates.requests.get", return_value=make_response(payload)):
        with pytest.raises(RatesFetchError, match="Unexpected response format") as exc_info:
            fetch_latest_rates()

    assert isinstance(exc_info.value.__cause__, ValueError)