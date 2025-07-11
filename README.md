# datetimebot

## Описание

Telegram-бот, который показывает дату, время, погоду в выбранном городе и курс доллара.

## Быстрый старт на Railway

1. **Подключите репозиторий к Railway**
2. **Добавьте переменные окружения:**
   - `TOKEN` — токен Telegram-бота
   - `OPENWEATHER_API_KEY` — API-ключ OpenWeather
   - `CITY` — город (например, Moscow)
3. **Procfile уже настроен**
4. **Деплой происходит автоматически после пуша**

## Локальный запуск

```bash
pip install -r requirements.txt
export TOKEN=ваш_токен
export OPENWEATHER_API_KEY=ваш_ключ
export CITY=Moscow
python3 telegram_datetime_bot.py
```