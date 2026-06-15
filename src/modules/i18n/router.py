from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db

router = APIRouter(prefix="/i18n", tags=["i18n"])

SUPPORTED_LOCALES = {
    "tr": {"name": "Turkce", "native": "Turkce"},
    "en": {"name": "English", "native": "English"},
    "ar": {"name": "Arabic", "native": "Arabic", "rtl": True},
    "de": {"name": "German", "native": "Deutsch"},
    "fr": {"name": "French", "native": "Francais"},
    "ru": {"name": "Russian", "native": "Russian"},
    "zh": {"name": "Chinese", "native": "Chinese"},
    "nl": {"name": "Dutch", "native": "Nederlands"},
}

SUPPORTED_CURRENCIES = {
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "decimals": 2},
    "USD": {"name": "US Dollar", "symbol": "$", "decimals": 2},
    "EUR": {"name": "Euro", "symbol": "€", "decimals": 2},
    "GBP": {"name": "British Pound", "symbol": "£", "decimals": 2},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "decimals": 2},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "decimals": 2},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "decimals": 2},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "decimals": 2},
}


@router.get("/locales")
async def list_locales():
    return SUPPORTED_LOCALES


@router.get("/currencies")
async def list_currencies():
    return SUPPORTED_CURRENCIES
