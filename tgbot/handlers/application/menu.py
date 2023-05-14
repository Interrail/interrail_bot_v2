from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from tgbot.keyboards.reply import application_keyboard


async def get_application(message: types.Message):
    await message.answer(text="Выберите заявку", reply_markup=application_keyboard)


def register_menu(dp: Dispatcher):
    dp.register_message_handler(get_application, Text(equals='📄 Заявки'))
