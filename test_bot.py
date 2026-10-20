import asyncio
import os
from dotenv import load_dotenv
from parser.price_api import fetch_eth_price

load_dotenv()


async def main():
    print("Проверяю источник цены...")
    data = await fetch_eth_price("ETH", "USD")
    print(
        f"✅ Успех: ${data['price']:.2f} (за 24ч: {data['percent_change_24h']:+.2f}%)"
    )
    print(f"   Источник: {data['source']}")


asyncio.run(main())
