from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply import start_keyboard
from tgbot.misc.states import Container


def get_container_info(container_name):
    # Check that the container name is 11 characters long
    if len(container_name) != 11:
        return "Invalid container name"

    # Extract the owner code, category and size code, and serial number from the container name
    owner_code = container_name[:3]
    category_and_size = container_name[3:7]
    serial_number = container_name[7:]

    # Define a dictionary of category codes and their corresponding container types
    category_codes = {
        "U": "Standard Dry Cargo Container",
        "J": "Standard Dry Cargo Container",
        "T": "Tank Container",
        "R": "Refrigerated Container",
        "P": "Open Top Container",
        "H": "Platform Container",
        "L": "Container for Cars and Light Vehicles",
        "G": "Container for Heavy Vehicles",
        "S": "Shelter Container",
        "D": "Tunnel Container",
        "O": "Open Sided Container",
        "N": "Container for Dangerous Goods",
        "F": "Flexible Intermediate Bulk Container",
        "B": "Bulk Container",
        "M": "Modular Expandable Container",
        "Y": "Other Container",
    }

    # Define a dictionary of size codes and their corresponding container lengths
    size_codes = {
        "1": "10 ft",
        "2": "20 ft",
        "3": "30 ft",
        "4": "40 ft",
        "5": "45 ft",
        "6": "48 ft",
        "7": "53 ft",
    }
    container_type = category_codes.get(category_and_size[0], "Unknown Container Type")
    container_size = size_codes.get(category_and_size[1], "Unknown Container Size")
    container_height = "High Cube" if category_and_size[2] == "H" else "Standard"
    container_max_gross_weight = int(category_and_size[3:]) * 1000
    container_owner = "Unknown Owner"  # Add code to lookup owner based on owner code

    # Create a dictionary of container specifications and return it
    container_info = {
        "Owner": container_owner,
        "Type": container_type,
        "Size": container_size,
        "Height": container_height,
        "Max Gross Weight": container_max_gross_weight,
        "Serial Number": serial_number,
    }

    return container_info


async def enter_container(message: Message):
    Container.container.set()
    await message.answer("Введите номер контейнера", reply_markup=start_keyboard)


async def get_container(message: Message, state):
    container_name = message.text
    container_info = get_container_info(container_name)
    await message.answer(container_info, reply_markup=start_keyboard)


def register_container(dp: Dispatcher):
    dp.register_message_handler(enter_container, lambda message: message.text == "Проверка Контейнера", state='*')
    dp.register_message_handler(get_container, state=Container.container)
