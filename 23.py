import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Message
from aiogram.filters import Command
import asyncio

referral_links = {}

kb = InlineKeyboardMarkup(inline_keyboard=[\
    [InlineKeyboardButton(text="Сократитель", web_app=WebAppInfo(url="https://as-opal.vercel.app/"))]
    ])

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token="7521199935:AAE6-z9bgumTHd6CTcgQNHqU5jiNrl8foOU")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    """Send a message with a button that opens the web app."""
    # Check if the user came through a referral link
    args = message.text.split()
    if len(args) > 1:
        ref_code = args[1]
        if ref_code in referral_links:
            ref_owner_id = referral_links[ref_code]["owner_id"]
            try:
                await bot.send_message(ref_owner_id, f"Пользователь {message.from_user.mention_html()} перешел по вашей реферальной ссылке!", parse_mode="HTML")
            except Exception as e:
                logger.error(f"Ошибка отправки уведомления: {e}")

    await message.answer(
        "Ты перешел по реферальной ссылке пользователя @catfrik",
        reply_markup=kb)

@dp.message(Command("ref"))
async def generate_ref_link(message: types.Message):
    """Generate a referral link and store it in the dictionary."""
    user_id = message.from_user.id
    ref_code = str(user_id)
    ref_link = f"https://t.me/as_opalbot?start={ref_code}"
    referral_links[ref_code] = {"owner_id": user_id, "ref_link": ref_link}
    await message.answer(f"Your referral link is: {ref_link}")

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=["message", "web_app_data"])

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")

