import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Message
from aiogram.filters import Command
import asyncio

kb = InlineKeyboardMarkup(inline_keyboard=[\
    [InlineKeyboardButton(text="Web app", web_app=WebAppInfo(url="https://valentine-for-girl.vercel.app"))]
    ])

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

referral_links = {}

bot = Bot(token="7963739821:AAH5tLZ8MuOtfjWkUJAycGL6nIyObs3RJnk")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    """Send a message with a button that opens the web app."""
    await message.answer(
        "Ты перешел по реферальной ссылке пользователя @catfrik",
        reply_markup=kb)

@dp.message(Command("ref"))
async def generate_ref_link(message: types.Message):
    """Generate a referral link and store it in the dictionary."""
    user_id = message.from_user.id
    if user_id in referral_links:
        ref_link = referral_links[user_id]
    else:
        ref_code = str(user_id)
        ref_link = f"https://t.me/bot?start={ref_code}"
        referral_links[user_id] = ref_link
    await message.answer(f"Your referral link is: {ref_link}")




async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=["message", "web_app_data"])


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
