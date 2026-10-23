# 💰Парсер - бот Эфириума (ETH) #
[![aiogram](https://img.shields.io/badge/aiogram-3.*-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![aiohttp](https://img.shields.io/badge/aiohttp-3.x-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white)](https://docs.aiohttp.org/)
[![APScheduler](https://img.shields.io/badge/APScheduler-3.x-6A1B9A?style=for-the-badge&logo=clockify&logoColor=white)](https://apscheduler.readthedocs.io/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-1.x-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)](https://github.com/theskumar/python-dotenv)

## Автор: **Владимир**, начинающий _python_ - разработчик ##
### Ссылки на *другие* мои проекты: [ai reviever](https://github.com/vlheadcrush06/ai_reviever-v2), [Эхо - бот](https://github.com/vlheadcrush06/ECHO-bot)


 ## ❓*Что умеет этот бот?*

- ⏰ Автоматическая проверка курса ETH каждые 10 минут через планировщик APScheduler.
- 📊 Отправка карточки с текущей ценой, изменением за 24 часа и временем обновления.
- 🌍 Работает без API-ключей и регистрации — используется публичный API CoinGecko.
- 🚀 Не требует VPN или прокси — доступен из любой страны.
- 🛡️ Устойчивость к сетевым сбоям: ошибки логируются, бот продолжает работу.
- 🐳 Готов к развёртыванию на VPS, в Docker или на бесплатном хостинге.

  **ВАЖНО!!!** если его разворачивать на сервере для работы на постоянной основе, требует периодического перезапуска (примерно раз в сутки),
или же написания специального софта, созданием которого сейчас занимаюсь.

## **❓Что необходимо для запуска?**

- **Python 3.9+**
- **pip** (менеджер пакетов Python)
- **Токен Telegram-бота** — получить у [@BotFather](https://t.me/BotFather)
- **Ваш `chat_id`** — узнать через [@userinfobot](https://t.me/userinfobot)

## 📦 Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/vlheadcrush06/ETH-parser-bot.git
cd eth_price_bot
```

### 2. Создать виртуальное окружение (рекомендуется)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
aiogram==3.*
aiohttp
APScheduler
python-dotenv
```

---

## ⚙️ Настройка

### 1. Создать файл `.env` в корне проекта

```env
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
CHAT_ID=123456789
```

| Переменная | Описание |
|---|---|
| `BOT_TOKEN` | Токен бота, полученный у @BotFather |
| `CHAT_ID` | ID чата или канала, куда присылать курс. Можно узнать у @userinfobot |

> ⚠️ **Не коммитьте `.env` в git.** Добавьте его в `.gitignore`.

### 2. Проверить `config.json`

```json
{
  "symbol": "ETH",
  "convert": "USD",
  "display_name": "Ethereum (ETH)"
}
```

| Поле | Описание |
|---|---|
| `symbol` | Тикер монеты: `ETH`, `BTC`, `SOL` и т.д. |
| `convert` | Валюта: `USD`, `EUR`, `RUB` |
| `display_name` | Отображаемое имя в сообщении |

---

## ▶️ Запуск

```bash
python main.py
```

В логах появится:
```
Бот запущен. Проверка курса ETH каждые 10 минут.
```

Первая проверка произойдёт через 10 минут. Чтобы проверить сразу — см. раздел [Тестирование](#-тестирование).

---

## 🧪 Тестирование

### Тест 1. Проверка API без Telegram


Запуск:

открываем терминал, пишем:

```bash
python test_bot.py
```

Ожидаемый вывод:
```
Цена ETH: $2345.67
Изменение за 24ч: +1.23%
Источник: CoinGecko
```

### Тест 2. Проверка отправки в Telegram


Запустите `python main.py`. Первая проверка сработает сразу при старте, а не через 10 минут.

### Сколько стоит развернуть бота на сервере?

| Хостинг | Стоимость | Комментарий |
|---|---|---|
| **VPS (Timeweb, Hetzner, Vultr)** | ~300–500 ₽/мес | Минимум: 1 CPU, 1 ГБ RAM. Идеально. |
| **Serv00** | Бесплатно | Подходит для небольших ботов, требует настройки |
| **Railway.app** | Есть бесплатный лимит | Хорошо для тестов, потом ~$5/мес |
| **Render.com** | Бесплатно | ⚠️ «Засыпает» через 15 минут — не подходит для long polling |

### Что проверить через сутки

```bash
# Процесс жив?
sudo systemctl status eth-bot

# Память (норма 50–150 МБ)
ps -o pid,rss,cmd -p $(pgrep -f main.py)

# Логи растут разумно?
du -sh bot.log

# Курс приходил каждые 10 минут?
grep "Курс отправлен" bot.log | tail -20
```

---

## ⚠️ Возможные проблемы

### `ModuleNotFoundError: No module named 'parser'`

**Причина:** запустили не из корня проекта.

**Решение:**
```bash
cd /путь/к/eth_parser_bot
python main.py
```

### `KeyError: 'BOT_TOKEN'` / `Unauthorized`

**Причина:** не создан `.env`, либо токен неверный.

**Решение:** проверьте, что `.env` лежит рядом с `main.py` и в нём правильный токен из @BotFather.

### `TelegramForbiddenError: bot was blocked by the user`

**Причина:** вы не нажали `/start` у бота, либо `CHAT_ID` указывает не на тот чат.

**Решение:** откройте бота в Telegram, отправьте `/start`, проверьте `CHAT_ID` через @userinfobot.

### `aiohttp.ClientResponseError: 429 Too Many Requests`

**Причина:** превышен лимит CoinGecko (~10–30 запросов/минуту).

**Решение:** для одного бота с интервалом 10 минут это невозможно. Если запущено несколько экземпляров с одного IP — увеличьте интервал или используйте другой API.

### `ConnectionError` / таймаут

**Причина:** нет интернета или CoinGecko временно недоступен.

**Решение:** бот продолжит работу — следующая проверка через 10 минут. Если ошибка повторяется — проверьте доступность `https://api.coingecko.com` из вашей сети.

### Бот работает, но не присылает сообщения

**Причина:** возможно, `.env` указывает на неверный `CHAT_ID`.

**Решение:** временно добавьте `print(os.getenv("CHAT_ID"))` в `main.py` при старте, проверьте значение.
