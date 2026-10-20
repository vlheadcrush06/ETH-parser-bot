from aiogram import Bot
from aiogram.enums import ParseMode


async def send_price_card(
    bot: Bot, chat_id: int | str, display_name: str, price_data: dict
):
    """
    Отправляет карточку с курсом ETH в Telegram.
    Цена форматируется с двумя знаками после запятой и разделителями тысяч.
    """
    price = price_data["price"]
    change = price_data.get("percent_change_24h")

    # Форматирование цены: 2 345.67
    price_str = f"{price:,.2f}".replace(",", " ")

    # Форматирование изменения за 24 часа (если есть)
    if change is not None:
        sign = "+" if change >= 0 else ""
        change_str = f"{sign}{change:.2f}%"
        change_icon = "📈" if change >= 0 else "📉"
    else:
        change_str = "н/д"
        change_icon = "➖"

    text = (
        f"<b>{display_name}</b>\n\n"
        f"💰 <b>Текущий курс:</b> ${price_str}\n"
        f"{change_icon} <b>Изменение за 24ч:</b> {change_str}\n\n"
        f"🕒 Обновлено: {price_data.get('last_updated', 'только что')}"
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
