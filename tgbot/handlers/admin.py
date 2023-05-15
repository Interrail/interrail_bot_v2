from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply import start_keyboard


async def admin_start(message: Message):
    await message.reply("Hello, admin!", reply_markup=start_keyboard)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
