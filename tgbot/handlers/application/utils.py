import random

import aiohttp
from aiogram.dispatcher import FSMContext
from docxtpl import DocxTemplate
from stdnum.iso6346 import compact, _iso6346_re, calc_check_digit


async def create_application_import_export_text(state: FSMContext, state_field: str, message=None,
                                                call_data=None):
    code_fields = ['application_type', 'terminal_name', 'container_status', 'container_type', 'container_owner',
                   'container_date', ]
    code_text_fields_translations = {
        'application_type': 'Заявка на',
        'terminal_name': 'Терминал',
        'container_status': 'Статус контейнера',
        'container_type': 'Тип контейнера',
        'container_owner': 'Собственник',
        'container_date': 'Дата',
    }
    text = ''
    if call_data is not None:
        await state.update_data({state_field: call_data})
    else:
        await state.update_data({state_field: message.text})
    user_data = await state.get_data()
    for count, field in enumerate(code_fields):
        text += f'{count + 1}. *{code_text_fields_translations[field]}*:{user_data[field]} \n'
        if field == state_field != code_fields[-1]:
            break
        if field == code_fields[-1]:
            text += f'{count + 1}. *Контейнера*: ?\n'
    return text


async def create_docx_template_import_export(containers, data):
    doc = DocxTemplate("tgbot/data/templates/Пустой бланк ИнтерРейл.docx")
    row_contents = []

    for count, container_number in enumerate(containers):
        row_contents.append(
            {"number": count + 1,
             "name": container_number,
             "type": data['container_type'],
             "status": data['container_status'],
             "owner": data['container_owner'],
             }
        )
    application_type = {
        'import': "завоз",
        'export': "вывоз"
    }
    context = {
        'application_type': application_type[data['application_type']],
        'date': data['container_date'],
        'number': random.randint(8000, 9000),
        't_name': data['terminal_name'],
        "row_contents": row_contents
    }
    doc.render(context)
    doc.save("tgbot/data/generated_doc.docx")


async def convert_docx_to_pdf():
    async with aiohttp.ClientSession() as session:
        data = {
            'files': open('tgbot/data/generated_doc.docx', 'rb')
        }
        async with session.post('https://image.interrail.uz/forms/libreoffice/convert', data=data) as resp:
            pdf_bytes = await resp.content.read()

            # Save the PDF file
            with open('tgbot/data/pdf/generated_pdf.pdf', 'wb') as f:
                f.write(pdf_bytes)


def validate_container(number):
    """Validate the given number (unicode) for conformity to ISO 6346."""
    number = compact(number)
    if len(number) != 11:
        return False, "Номер имеет недопустимую длину."
    if not _iso6346_re.match(number):
        return False, "Номер имеет недопустимый формат."
    if calc_check_digit(number[:-1]) != number[-1]:
        return False, "Номер не является правильным"
    return True, "The number is valid."
