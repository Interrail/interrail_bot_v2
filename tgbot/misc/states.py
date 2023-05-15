from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplicationImportExport(StatesGroup):
    application_type = State()
    terminal_name = State()
    container_status = State()
    container_type = State()
    container_owner = State()
    container_date = State()
    container_number = State()
    get_application = State()
    edit_application = State()
    task = State()
