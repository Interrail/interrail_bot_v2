import aiohttp
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from tgbot.config import load_config
from tgbot.filters.user import UserAccess
from tgbot.handlers.application.utils import create_application_import_export_text, create_docx_template_import_export, \
    convert_docx_to_pdf, validate_container
from tgbot.keyboards.inline import inline_terminal_keyboard, inline_container_status_keyboard, \
    inline_container_type_keyboard, inline_container_owner_keyboard, inline_get_pdf_for_import_export
from tgbot.keyboards.reply import start_keyboard
from tgbot.misc.states import ApplicationImportExport


async def choose_application_type(message: types.Message, state: FSMContext):
    if message.text.split(' ')[-1] in ['завоз', 'вывоз']:
        application_type = {'завоз': 'import', 'вывоз': 'export', }
        await state.finish()
        await state.update_data(application_type=application_type[message.text.split(' ')[-1]])
        await ApplicationImportExport.terminal_name.set()
        await message.answer(text=message.text, reply_markup=inline_terminal_keyboard)
    else:
        await message.answer(text=message.text)


async def get_terminal(call: CallbackQuery, state: FSMContext):
    await ApplicationImportExport.container_status.set()
    text = await create_application_import_export_text(state=state, state_field='terminal_name', call_data=call.data)
    await call.message.edit_text(text=text, reply_markup=inline_container_status_keyboard, parse_mode='Markdown')


async def get_container_status(call: CallbackQuery, state: FSMContext):
    await ApplicationImportExport.container_type.set()
    text = await create_application_import_export_text(state=state, state_field='container_status', call_data=call.data)
    await call.message.edit_text(text=text, reply_markup=inline_container_type_keyboard, parse_mode='Markdown')


async def get_container_type(call: CallbackQuery, state: FSMContext):
    await ApplicationImportExport.container_owner.set()
    text = await create_application_import_export_text(state=state, state_field='container_type', call_data=call.data)
    await call.message.edit_text(text=text, reply_markup=inline_container_owner_keyboard, parse_mode='Markdown')


#
#
async def get_container_owner(call: CallbackQuery, state: FSMContext):
    await ApplicationImportExport.container_date.set()
    text = await create_application_import_export_text(state=state, state_field='container_owner', call_data=call.data)
    await call.message.edit_text(text=text, reply_markup=await SimpleCalendar().start_calendar(), parse_mode='Markdown')


#
#

async def get_start_date_history(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)

    if selected:
        await ApplicationImportExport.next()
        await state.update_data(container_date=date.strftime("%Y-%m-%d"))
        text = await create_application_import_export_text(state=state, state_field='container_date',
                                                           call_data=date.strftime("%Y-%m-%d"))
        await callback_query.message.edit_text(text=text, parse_mode='Markdown')


async def get_container_number(message: types.Message, state: FSMContext):
    containers = message.text.upper().split('\n')
    incorrect_containers = []
    for count, container_number in enumerate(containers):
        if not validate_container(container_number)[0]:
            incorrect_containers.append({
                'container_number': container_number,
                'error': validate_container(container_number)[1]
            })
    if incorrect_containers:
        text = 'Некорректные номера контейнеров:\n'
        for incorrect_container in incorrect_containers:
            text += '<b>{}</b> {}\n'.format(incorrect_container['container_number'], incorrect_container['error'])
        await message.answer(text=text)

    else:

        await ApplicationImportExport.get_application.set()
        await state.update_data(container_number=containers)
        container_numbers = ''
        for count, container_number in enumerate(containers):
            container_numbers += "{} {} \n".format(count + 1, container_number)
        user_data = await state.get_data()
        text = '''
    *Заявка*{}
    *Терминал:*{}
    *Статус контейнера:*{}
    *Тип контейнера:*{}
    *Собственник:*{}
    *Дата:*{}
    *Контейнера:*
    {}'''.format(user_data['application_type'], user_data['terminal_name'],
                 user_data['container_status'], user_data['container_type'],
                 user_data['container_owner'], user_data['container_date'], container_numbers)
        await state.update_data(task=text)
        await message.answer(text=text, reply_markup=inline_get_pdf_for_import_export, parse_mode='Markdown')


async def add_container(call: CallbackQuery, state: FSMContext):
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    async with state.proxy() as data:
        containers = data['container_number']
        await create_docx_template_import_export(containers, data)
        await convert_docx_to_pdf()
    if data['application_type'] == 'import':
        file = types.InputFile("tgbot/data/pdf/generated_pdf.pdf",
                               filename="Заявка_" + data['terminal_name'] + "_" + 'Завоз' + ".pdf")
    else:
        file = types.InputFile("tgbot/data/pdf/generated_pdf.pdf",
                               filename="Заявка_" + data['terminal_name'] + "_" + 'Вывоз' + ".pdf")

    sending_data = {
        'containers': containers,
        'container_type': data['container_type'],
        'telegram_id': call.from_user.id,
        'terminal': data['terminal_name'],
        'arrival_date': data['container_date']
    }

    if data['container_status'] == 'Груженный':
        sending_data['is_laden'] = True
    else:
        sending_data['is_laden'] = False

    async with aiohttp.ClientSession() as session:
        async with session.post('https://order.interrail.uz/terminal/bot/create/', data=sending_data) as resp:
            if resp.status == 201:
                await state.finish()
                await bot.send_document(call.from_user.id, file, reply_markup=start_keyboard)
            else:
                await state.finish()
                await bot.send_message(call.from_user.id, 'Произошла ошибка, свяжитесь с администратором')


def register_application(dp: Dispatcher):
    dp.register_message_handler(choose_application_type,
                                lambda message: message.text in ["⬅ Заявка на завоз", "➡ Заявка на вывоз"],
                                UserAccess(),
                                state='*')

    dp.register_callback_query_handler(get_terminal, state=ApplicationImportExport.terminal_name)
    dp.register_callback_query_handler(get_container_status,
                                       state=ApplicationImportExport.container_status)
    dp.register_callback_query_handler(get_container_type, state=ApplicationImportExport.container_type)
    dp.register_callback_query_handler(get_container_owner,
                                       state=ApplicationImportExport.container_owner)
    dp.register_callback_query_handler(get_start_date_history,
                                       simple_cal_callback.filter(),
                                       state=ApplicationImportExport.container_date)
    dp.register_message_handler(get_container_number, state=ApplicationImportExport.container_number)
    dp.register_callback_query_handler(add_container, state=ApplicationImportExport.get_application, )
