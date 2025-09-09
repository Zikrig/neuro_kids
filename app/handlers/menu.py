from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext
from app.keyboards import main_menu_keyboard, mult_table_branches_keyboard
from app.states import AdminStates
import os
import json
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import re

# Список ID админов
ADMIN_IDS = [184374602]

router = Router()

def load_texts():
    with open("data/texts.json", encoding="utf-8") as f:
        return json.load(f)

def save_texts(texts):
    with open("data/texts.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

# Функции для работы с сервисами
def load_service_data():
    try:
        with open('data/service_details.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_service_data(service_data):
    with open('data/service_details.json', 'w', encoding='utf-8') as f:
        json.dump(service_data, f, ensure_ascii=False, indent=2)

texts = load_texts()

# @router.callback_query(F.data == "start")
# async def after_start(callback: CallbackQuery):
#     if os.path.exists("data/image10.png"):
#         await callback.message.answer_photo(
#             FSInputFile("data/image10.png"),
#             caption=texts["greeting"],
#             reply_markup=main_menu_keyboard()
#         )
#         return
#     await callback.message.answer(
#         texts["greeting"],
#         reply_markup=main_menu_keyboard()
#     )

@router.message(Command("start"))
async def cmd_start(message: Message):
    if os.path.exists("data/image10.png"):
        await message.answer_photo(
            FSInputFile("data/image10.png"),
            caption=texts["greeting"],
            reply_markup=main_menu_keyboard()
        )
        return
    await message.answer(
        texts["greeting"],
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "get_guide")
async def get_guide(callback: CallbackQuery):
    guide_path = "data/guide.pdf"
    if os.path.exists(guide_path):
        await callback.message.answer_document(FSInputFile(guide_path))
    else:
        await callback.message.answer("Файл guide.pdf не найден.")
    await callback.message.answer(
        texts["guide_prompt"],
        reply_markup=main_menu_keyboard()
    )
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer(
        texts["main_menu"],
        reply_markup=main_menu_keyboard()
    )
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

@router.callback_query(F.data == "about")
async def about_center(callback: CallbackQuery):
    await callback.message.answer(
        texts["about"],
        reply_markup=main_menu_keyboard()
    )
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):
    await callback.message.answer(
        texts["contacts"],
        reply_markup=main_menu_keyboard()
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == "get_guide")
async def get_guide(callback: CallbackQuery):
    guide_path = "data/guide.pdf"
    if os.path.exists(guide_path):
        await callback.message.answer_document(FSInputFile(guide_path))
    else:
        await callback.message.answer("Файл guide.pdf не найден.")
    await callback.message.answer(
        texts["guide_prompt"],
        reply_markup=main_menu_keyboard()
    )
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data == "appoint_mult_table")
async def appoint_mult_table_link(callback: CallbackQuery, state: FSMContext):
    url = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"
    text = 'Для записи воспользуйтесь <a href="{}">формой</a>.'
    await callback.message.answer(text.format(url), parse_mode="HTML", reply_markup=main_menu_keyboard())
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

# --- Админский режим ---
@router.message(Command("admin"))
async def admin_services(message: Message, state: FSMContext):
    # if message.from_user.id not in ADMIN_IDS:
    #     await message.answer("Нет доступа.")
    #     return
    
    service_data = load_service_data()
    service_details = service_data.get('service_details', {})
    online_details = service_data.get('online_details', {})
    
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки для всех услуг
    for service_key in service_details.keys():
        builder.add(InlineKeyboardButton(
            text=service_details[service_key].get("title", service_key),
            callback_data=f"admin_service_{service_key}"
        ))
    
    # Добавляем кнопку для онлайн-формата
    builder.add(InlineKeyboardButton(
        text="Онлайн-формат",
        callback_data="admin_service_online_details"
    ))
    
    builder.add(InlineKeyboardButton(
        text="↩️ Назад",
        callback_data="admin_cancel"
    ))
    
    builder.adjust(1)
    
    await message.answer(
        "Выберите услугу для редактирования:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AdminStates.choosing_service)

@router.callback_query(F.data.startswith("admin_service_"))
async def admin_choose_service(callback: CallbackQuery, state: FSMContext):
    service_key = callback.data.split("admin_service_")[1]
    await state.update_data(service_key=service_key)
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Название",
        callback_data="admin_field_title"
    ))
    # builder.add(InlineKeyboardButton(
    #     text="Изображение",
    #     callback_data="admin_field_image"
    # ))
    builder.add(InlineKeyboardButton(
        text="Описание",
        callback_data="admin_field_desc"
    ))
    builder.add(InlineKeyboardButton(
        text="↩️ Назад",
        callback_data="admin_back_to_services"
    ))
    
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"Выберите поле для редактирования услуги <b>{service_key}</b>:",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AdminStates.choosing_field)

@router.callback_query(F.data.startswith("admin_field_"))
async def admin_choose_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("admin_field_")[1]
    await state.update_data(field=field)
    
    # Получаем текущее значение
    data = await state.get_data()
    service_key = data.get("service_key")
    
    service_data = load_service_data()
    
    if service_key == "online_details":
        current_value = service_data.get('online_details', {}).get(field, "")
    else:
        current_value = service_data.get('service_details', {}).get(service_key, {}).get(field, "")
    
    await callback.message.edit_text(
        f"Текущее значение поля <b>{field}</b> для услуги <b>{service_key}</b>:\n\n"
        f"{current_value}\n\n"
        f"Пожалуйста, введите новое значение:",
        parse_mode="HTML"
    )
    
    await state.set_state(AdminStates.entering_value)

@router.message(AdminStates.entering_value)
async def admin_set_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    service_key = data.get("service_key")
    field = data.get("field")
    
    # Загружаем текущие данные
    service_data = load_service_data()
    
    # Обновляем значение
    if service_key == "online_details":
        if 'online_details' not in service_data:
            service_data['online_details'] = {}
        service_data['online_details'][field] = new_value
    else:
        if 'service_details' not in service_data:
            service_data['service_details'] = {}
        if service_key not in service_data['service_details']:
            service_data['service_details'][service_key] = {}
        service_data['service_details'][service_key][field] = new_value
    
    # Сохраняем изменения
    save_service_data(service_data)
    
    await message.answer(
        f"Значение для поля <b>{field}</b> услуги <b>{service_key}</b> успешно обновлено!",
        parse_mode="HTML"
    )
    
    # Возвращаемся к выбору услуги
    await admin_services(message, state)

@router.callback_query(F.data == "admin_back_to_services")
async def admin_back_to_services(callback: CallbackQuery, state: FSMContext):
    await admin_services(callback.message, state)

@router.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Редактирование отменено.")