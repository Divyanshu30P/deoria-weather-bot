import os
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

LAT = 26.5048
LON = 83.7810

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

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

        w = requests.get(weather_url).json()
        a = requests.get(aqi_url).json()

        msg = (
            "📍 *Deoria, Uttar Pradesh*\n\n"
            f"🌡 Temp: {w['main']['temp']}°C\n"
            f"🤗 Feels Like: {w['main']['feels_like']}°C\n"
            f"💧 Humidity: {w['main']['humidity']}%\n"
            f"🌥 Condition: {w['weather'][0]['description'].title()}\n\n"
            f"🌫 AQI Level: {a['list'][0]['main']['aqi']}"
        )

        await update.message.reply_markdown(msg)

    except Exception:
        await update.message.reply_text("⚠️ Unable to fetch data.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("weather", weather))

@app.post("/api/bot")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
