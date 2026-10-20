import aiohttp
import ssl
import certifi
import logging

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"


def _make_connector() -> aiohttp.TCPConnector:
    """Явно использует обновлённый файл сертификатов из certifi."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return aiohttp.TCPConnector(ssl=ssl_context)


async def fetch_eth_price(symbol: str = "ETH", convert: str = "USD") -> dict:
    """Пробует CoinGecko, при ошибке — Binance. Оба API бесплатны и без ключа."""
    try:
        result = await _fetch_coingecko(symbol, convert)
        logger.info("Цена получена с CoinGecko")
        return result
    except Exception as e:
        logger.warning(f"CoinGecko недоступен ({e}), пробую Binance...")

    result = await _fetch_binance(symbol)
    logger.info("Цена получена с Binance")
    return result


async def _fetch_coingecko(symbol: str, convert: str) -> dict:
    coin_id = "ethereum" if symbol.upper() == "ETH" else symbol.lower()
    currency = convert.lower()
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true",
    }
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(
        connector=_make_connector(), timeout=timeout
    ) as session:
        async with session.get(COINGECKO_URL, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()

    if coin_id not in data:
        raise ValueError(f"Неожиданный ответ от CoinGecko: {data}")

    quote = data[coin_id]
    change = quote.get(f"{currency}_24h_change")
    return {
        "price": float(quote[currency]),
        "percent_change_24h": float(change) if change is not None else None,
        "source": "CoinGecko",
    }


async def _fetch_binance(symbol: str) -> dict:
    pair = f"{symbol.upper()}USDT"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(
        connector=_make_connector(), timeout=timeout
    ) as session:
        async with session.get(BINANCE_URL, params={"symbol": pair}) as resp:
            resp.raise_for_status()
            data = await resp.json()

    return {
        "price": float(data["lastPrice"]),
        "percent_change_24h": float(data["priceChangePercent"]),
        "source": "Binance",
    }
