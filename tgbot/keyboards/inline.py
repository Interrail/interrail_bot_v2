from aiogram import types
from aiogram.types import InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('🏢 ULS', callback_data='ULS')
inline_btn_2 = InlineKeyboardButton('🏢 FTT', callback_data='FTT')
inline_btn_3 = InlineKeyboardButton('🏢 ATT', callback_data='ATT')
inline_btn_4 = InlineKeyboardButton('🏢 TSIG', callback_data='TSIG')
inline_btn_5 = InlineKeyboardButton('🏢 FDTP', callback_data='FDTP')

inline_terminal_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_terminal_keyboard.add(inline_btn_1, inline_btn_2)
inline_terminal_keyboard.add(inline_btn_3, inline_btn_4)
inline_terminal_keyboard.add(inline_btn_5)

inline_get_pdf_btn = InlineKeyboardButton('📄 Получить', callback_data='Получить')
inline_edit_pdf_btn = InlineKeyboardButton('📝 Изменить', callback_data='Изменить')

inline_get_pdf_for_import_export = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_get_pdf_for_import_export.add(inline_get_pdf_btn)

inline_get_pdf = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_get_pdf.add(inline_get_pdf_btn)
inline_get_pdf.add(inline_edit_pdf_btn)

inline_btn_1 = InlineKeyboardButton('🚚 Порожний', callback_data='Порожний')
inline_btn_2 = InlineKeyboardButton('🚛 Груженный', callback_data='Груженный')

inline_container_status_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_container_status_keyboard.add(inline_btn_1, inline_btn_2)

inline_btn_1 = InlineKeyboardButton('📦 20 фут', callback_data='20')
inline_btn_2 = InlineKeyboardButton('📦 40 фут', callback_data='40')
inline_btn_3 = InlineKeyboardButton('📦 45 фут', callback_data='45')

inline_container_type_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_container_type_keyboard.add(inline_btn_1)
inline_container_type_keyboard.add(inline_btn_2)
inline_container_type_keyboard.add(inline_btn_3)

inline_btn_1 = InlineKeyboardButton('🚅 INTERRAIL SERVICES AG', callback_data='INTERRAIL SERVICES AG')
inline_container_owner_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
inline_container_owner_keyboard.add(inline_btn_1)