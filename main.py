import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

schedule = [
    ("09:50", "Kompyuterga tayyorlan: Word hujjati, shrift, PDF"),
    ("17:20", "Ichki ishlar: Ma’muriy kodeksni och, yozma topshiriqni bajargin"),
    ("19:50", "Jismoniy mashq: Plank, Push-up, press, burpee"),
    ("21:50", "Word yoki Excel topshirigʻini tugatish va tekshirish"),
    ("22:50", "Tahlil yozish va kunni xulosa qilish vaqti")
]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Abrorning eslatma boti ishga tushdi.")

def schedule_messages():
    for time_str, text in schedule:
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_reminder, 'cron', hour=hour, minute=minute, args=[text])

async def send_reminder(text):
    if CHAT_ID:
        await bot.send_message(chat_id=CHAT_ID, text=f"⏰ {text}")

if name == 'main':
    schedule_messages()
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
