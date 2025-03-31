from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import Application, CommandHandler
import datetime

TELEGRAM_BOT_TOKEN = "YOUR-API-TOKEN-FROM-TELEGRAM"

async def get_weather():
    today = datetime.date.today()
    formatted_today = today.strftime('%d-%m-%Y')
    day_name = today.strftime("%A")

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.accuweather.com/en/in/mussoori/1-196520_1_al/current-weather/1-196520_1_al', timeout=60000)
        temp = await page.locator('div.display-temp').text_content()
        await browser.close()
    
    return f"🌤️ Temperature of Mussoorie on {day_name}, {formatted_today}: {temp}"

async def start(update: Update, context):
    await update.message.reply_text("Hello! Type /weather to get Mussoorie's temperature.")

async def weather(update: Update, context):
    weather_info = await get_weather()
    await update.message.reply_text(weather_info)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
