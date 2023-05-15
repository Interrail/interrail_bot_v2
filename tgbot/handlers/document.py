import re

import aiohttp
from aiogram import Dispatcher, types
from aiogram.types import ContentType

from tgbot.filters.user import IsGroup


async def add_file(message: types.Message):
    container_number = str(message.document.file_name)[:11]
    pattern = re.compile("([a-zA-Z]{3})([UJZujz])(\d{6})(\d)")
    if pattern.match(container_number):
        file = await message.bot.get_file(message.document.file_id)
        helo = await message.bot.download_file(file.file_path)
        helo.name = str(message.document.file_name)[:11] + '.pdf'

        status = ''
        async with aiohttp.ClientSession() as session:
            sending_data = {
                'container_name': container_number,
                'container_document': helo
            }

            async with session.post('https://order.interrail.uz/terminal/bot/container/add_document/',
                                    data=sending_data) as resp:
                status = resp.status

        if status == 201:
            text = str(container_number) + ' сохранён'
            await message.reply(text)
        else:
            await message.reply("Контейнер не сохранён  в системе")


def register_document(dp: Dispatcher):
    dp.register_message_handler(add_file, IsGroup(), content_types=ContentType.DOCUMENT, state='*')
