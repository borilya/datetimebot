import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
import locale
import requests
import xml.etree.ElementTree as ET
import os

# Установим русскую локаль для дней недели
try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except locale.Error:
    pass  # На MacOS может не быть русской локали, тогда будет на английском

TOKEN = os.environ.get('TOKEN')
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITY = os.environ.get('CITY', 'Moscow')

async def reply_with_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Получено сообщение!')
    now = datetime.now()
    date_str = now.strftime('%d.%m.%Y')
    weekday_str = now.strftime('%A')
    time_str = now.strftime('%H:%M:%S')

    # Получаем погоду
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru'
    try:
        weather_resp = requests.get(weather_url, timeout=5)
        weather_data = weather_resp.json()
        if weather_resp.status_code == 200:
            temp = weather_data['main']['temp']
            desc = weather_data['weather'][0]['description']
            weather_str = f'Погода в {CITY}: {temp:+.0f}°C, {desc}'
        else:
            weather_str = f'Не удалось получить погоду (код {weather_resp.status_code}): {weather_data}'
    except Exception as e:
        weather_str = f'Ошибка при получении погоды: {e}'

    # Получаем курс доллара
    try:
        rate_str = get_usd_rub_cbr()
    except Exception as e:
        rate_str = f'Ошибка при получении курса доллара: {e}'

    response = f'Сегодня: {date_str}\nДень недели: {weekday_str}\nВремя: {time_str}\n{weather_str}\n{rate_str}'
    await update.message.reply_text(response)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name if update.effective_user else "Пользователь"
    greeting = f"Привет, {user_first_name}!\n"
    now = datetime.now()
    date_str = now.strftime('%d.%m.%Y')
    weekday_str = now.strftime('%A')
    time_str = now.strftime('%H:%M:%S')

    # Получаем погоду
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru'
    try:
        weather_resp = requests.get(weather_url, timeout=5)
        weather_data = weather_resp.json()
        if weather_resp.status_code == 200:
            temp = weather_data['main']['temp']
            desc = weather_data['weather'][0]['description']
            weather_str = f'Погода в {CITY}: {temp:+.0f}°C, {desc}'
        else:
            weather_str = f'Не удалось получить погоду (код {weather_resp.status_code}): {weather_data}'
    except Exception as e:
        weather_str = f'Ошибка при получении погоды: {e}'

    # Получаем курс доллара
    try:
        rate_str = get_usd_rub_cbr()
    except Exception as e:
        rate_str = f'Ошибка при получении курса доллара: {e}'

    response = greeting + f'Сегодня: {date_str}\nДень недели: {weekday_str}\nВремя: {time_str}\n{weather_str}\n{rate_str}'
    await update.message.reply_text(response)

def get_usd_rub_cbr():
    try:
        resp = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', timeout=5)
        tree = ET.fromstring(resp.content)
        for valute in tree.findall('Valute'):
            if valute.find('CharCode').text == 'USD':
                return float(valute.find('Value').text.replace(',', '.'))
        return None
    except Exception as e:
        return f'Ошибка при получении курса ЦБ: {e}'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_with_datetime))
    app.run_polling() 