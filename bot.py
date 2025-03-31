from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import Application, CommandHandler
import datetime

TELEGRAM_BOT_TOKEN = "YOUR-API-TOKEN-FROM-TELEGRAM" 
#search @botfather on telegram, and /start then /newbot to make a new bot, 
#then you'll be asked to name your bot and then set a username,
#afterward it will provide you a api code, keep it safe

async def get_weather():
    today = datetime.date.today() #it will show today's date
    formatted_today = today.strftime('%d-%m-%Y') #this will show the date in dd:mm:yy format
    day_name = today.strftime("%A") #this will print day's name

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True) #whole process like opening of browser and searching will be hidden
        page = await browser.new_page() #opens a browser 
        await page.goto('https://www.accuweather.com/en/in/mussoori/1-196520_1_al/current-weather/1-196520_1_al', timeout=60000)
        temp = await page.locator('div.display-temp').text_content()
        await browser.close() #closes the browser when the scraping is completed
    
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
