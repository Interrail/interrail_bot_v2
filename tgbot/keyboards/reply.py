from aiogram import types

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
start_keyboard.add("📄 Заявки")

application_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
application_keyboard.add('⬅ Заявка на завоз')
application_keyboard.add('➡ Заявка на вывоз')
