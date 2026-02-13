import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Записаться", callback_data="book")]
    ])
    await message.answer(
        "Привет 💛\nЯ мастер шугаринга и восковой эпиляции.\nВыберите действие:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "book")
async def choose_service(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ноги полностью", callback_data="service_legs")],
        [InlineKeyboardButton(text="Бикини", callback_data="service_bikini")]
    ])
    await callback.message.answer("Выберите услугу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("service_"))
async def choose_time(callback: types.CallbackQuery):
    service = callback.data.split("_")[1]
    user_data[callback.from_user.id] = {"service": service}

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пн 10:00", callback_data="time_10")],
        [InlineKeyboardButton(text="Пн 14:00", callback_data="time_14")]
    ])
    await callback.message.answer("Выберите время:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("time_"))
async def confirm(callback: types.CallbackQuery):
    time = callback.data.split("_")[1]
    user_id = callback.from_user.id

    user_data[user_id]["time"] = time
    service = user_data[user_id]["service"]

    await callback.message.answer(
        f"Вы записаны на {service} в {time} 🥰\nЯ свяжусь с вами для подтверждения."
    )

    await bot.send_message(
        ADMIN_ID,
        f"Новая запись!\nУслуга: {service}\nВремя: {time}\nКлиент: @{callback.from_user.username}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
