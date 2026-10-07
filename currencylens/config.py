"""Central settings for the CurrencyLens pipeline."""

from pathlib import Path

# Extract information from Frankfurter API Base 
# Uses "EUR" has base currency for comparation
# Timout after 10 seconds if anything goes wrong
API_BASE_URL = "https://api.frankfurter.dev/v1"
BASE_CURRENCY = "EUR"
REQUEST_TIMEOUT_SECONDS = 10

# All 30 currencies supported by Frankfurt API
TARGET_CURRENCIES = {
  "AUD": "Australian Dollar",
  "BRL": "Brazilian Real",
  "CAD": "Canadian Dollar",
  "CHF": "Swiss Franc",
  "CNY": "Chinese Renminbi Yuan",
  "CZK": "Czech Koruna",
  "DKK": "Danish Krone",
  "GBP": "British Pound",
  "HKD": "Hong Kong Dollar",
  "HUF": "Hungarian Forint",
  "IDR": "Indonesian Rupiah",
  "ILS": "Israeli New Shekel",
  "INR": "Indian Rupee",
  "ISK": "Icelandic Króna",
  "JPY": "Japanese Yen",
  "KRW": "South Korean Won",
  "MXN": "Mexican Peso",
  "MYR": "Malaysian Ringgit",
  "NOK": "Norwegian Krone",
  "NZD": "New Zealand Dollar",
  "PHP": "Philippine Peso",
  "PLN": "Polish Złoty",
  "RON": "Romanian Leu",
  "SEK": "Swedish Krona",
  "SGD": "Singapore Dollar",
  "THB": "Thai Baht",
  "TRY": "Turkish Lira",
  "USD": "United States Dollar",
  "ZAR": "South African Rand",
                        }

# Load directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "currencylens.db"

# Analyse window
MOVING_AVERAGE_WINDOWS = (7, 30)
