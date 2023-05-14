from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import start_keyboard


async def user_start(message: Message, state: FSMContext):
    await state.finish()

    await message.reply("Вас приветствует ИнтерРейл бот!", reply_markup=start_keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
