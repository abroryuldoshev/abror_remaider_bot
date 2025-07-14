import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
import os
from datetime import datetime

API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

schedule = [
    ("09:50", "Kompyuterga tayyorlan: Word hujjati, shrift, PDF"),
    ("17:20", "Ichki ishlar: Ma’muriy kodeks, yozma topshiriq"),
    ("19:50", "Jismoniy mashq: Plank, Push-up, press, burpee"),
    ("21:50", "Word yoki Excel topshirig‘i"),
    ("22:50", "Tahlil yozish va kun xulosasi")
]

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton("✅ Bajarildi", callback_data="done"))
keyboard.add(types.InlineKeyboardButton("❌ O‘tkazib yuborildi", callback_data="skip"))

@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.reply("Salom Abror! Eslatma boti ishga tushdi.")

@dp.callback_query_handler()
async def cb_handler(call: types.CallbackQuery):
    if call.data == "done":
        await call.message.answer("Zo‘r — bajarildi ✅")
    elif call.data == "skip":
        await call.message.answer("O‘tkazib yuborildi ❌")

def setup_schedule():
    for t, txt in schedule:
        hr, mn = map(int, t.split(":"))
        scheduler.add_job(send_reminder, 'cron', hour=hr, minute=mn, args=[txt])

async def send_reminder(text):
    await bot.send_message(CHAT_ID, f"⏰ {text}", reply_markup=keyboard)

if name == "main":
    setup_schedule()
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
