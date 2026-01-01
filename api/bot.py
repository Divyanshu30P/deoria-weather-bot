import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Deoria, Uttar Pradesh coordinates
LAT = 26.5048
LON = 83.7810

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 Deoria Weather Bot\n\nUse /weather to get weather + AQI."
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric"
        )

        aqi_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution?"
            f"lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}"
        )

        weather = requests.get(weather_url).json()
        aqi = requests.get(aqi_url).json()

        msg = (
            "📍 *Deoria, Uttar Pradesh*\n\n"
            f"🌡 Temp: {weather['main']['temp']}°C\n"
            f"🤗 Feels Like: {weather['main']['feels_like']}°C\n"
            f"💧 Humidity: {weather['main']['humidity']}%\n"
            f"🌥 Condition: {weather['weather'][0]['description'].title()}\n\n"
            f"🌫 AQI Level: {aqi['list'][0]['main']['aqi']}"
        )

        await update.message.reply_markdown(msg)

    except Exception:
        await update.message.reply_text("⚠️ Unable to fetch data.")

def handler(request):
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    update = Update.de_json(request.json, application.bot)
    application.process_update(update)

    return {"statusCode": 200}
