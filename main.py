import asyncio
import json
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from parser.price_api import fetch_eth_price
from notifier.telegram_sender import send_price_card

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def check_price():
    """Основная задача: получить курс ETH и отправить в Telegram."""
    logger.info("Запрос курса ETH...")
    try:
        price_data = await fetch_eth_price(
            symbol=config["symbol"],
            convert=config["convert"],
        )
        await send_price_card(
            bot,
            CHAT_ID,
            display_name=config["display_name"],
            price_data=price_data,
        )
        logger.info(f"Курс отправлен: ${price_data['price']:.2f}")
    except Exception as e:
        logger.error(f"Ошибка при получении курса: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    # next_run_time=None означает, что первый запуск произойдёт через 10 минут,
    # а не мгновенно при старте. Если хотите проверить сразу — уберите этот параметр.
    scheduler.add_job(check_price, "interval", minutes=10)
    await check_price()
    scheduler.start()

    logger.info("Бот запущен. Проверка курса ETH каждые 10 минут.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
