from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from app.keyboards import main_menu_keyboard
from app.keyboards import mult_table_branches_keyboard
import os
import json
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import re

ADMIN_ID = 184374602  # Замените на свой Telegram user_id

router = Router()

def load_texts():
    with open("data/texts.json", encoding="utf-8") as f:
        return json.load(f)

def save_texts(texts):
    with open("data/texts.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

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

@router.callback_query(F.data == "info")
async def useful_info(callback: CallbackQuery):
    checklists = [f"data/checklist{i}.pdf" for i in range(1, 6)]
    for checklist in checklists:
        if os.path.exists(checklist):
            await callback.message.answer_document(FSInputFile(checklist))
        else:
            await callback.message.answer(f"Файл {checklist} не найден.")
    await callback.message.answer(
        texts["info_prompt"],
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
async def start_mult_table_appointment(callback: CallbackQuery, state):
    await state.set_state("mult_table_name")
    await callback.message.answer("Ваше имя:")

@router.message(StateFilter("mult_table_name"))
async def mult_table_name(message: Message, state):
    # Проверка: только буквы, минимум 2 символа
    if not re.match(r"^[А-Яа-яA-Za-zЁё\-\s]{2,}$", message.text.strip()):
        await message.answer("Пожалуйста, введите корректное имя (только буквы, не менее 2 символов).")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state("mult_table_phone")
    await message.answer("Ваш контактный телефон:")

@router.message(StateFilter("mult_table_phone"))
async def mult_table_phone(message: Message, state):
    # Простейшая проверка на телефон (11 цифр, допускается +7, 8, пробелы, дефисы)
    phone = re.sub(r"[^0-9]", "", message.text)
    if not (10 <= len(phone) <= 12):
        await message.answer("Пожалуйста, введите корректный номер телефона.")
        return
    await state.update_data(phone=message.text.strip())
    await state.set_state("mult_table_age")
    await message.answer("Возраст ребенка (полных лет):")

@router.message(StateFilter("mult_table_age"))
async def mult_table_age(message: Message, state):
    # Проверка: только число, 1-24
    try:
        age = int(message.text.strip())
        if not (1 <= age < 25):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите возраст от 1 до 24 лет.")
        return
    await state.update_data(age=age)
    await state.set_state("mult_table_branch")
    await message.answer("Выберите удобный филиал в г. Москва:", reply_markup=mult_table_branches_keyboard())

@router.callback_query(StateFilter("mult_table_branch"), F.data.startswith("mult_branch_"))
async def mult_table_branch(callback: CallbackQuery, state):
    branch_index = int(callback.data.split("_", 2)[2])
    branches = ["Отрадное (Москва)", "Молодежная (Москва)"]
    await state.update_data(branch=branches[branch_index])
    data = await state.get_data()
    await callback.message.answer(
        f"Спасибо за заявку, {data.get('name', '')}!\n"
        f"Мы свяжемся с вами в ближайшее время\n\n"
        f"Данные для отправки в CRM:\n"
        f"Услуга: ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ДНЕЙ\n"
        f"Телефон: {data.get('phone', '')}\n"
        f"Возраст ребенка: {data.get('age', '')}\n"
        f"Филиал: {data.get('branch', '')}",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()

# --- Админский режим ---

@router.message(Command("admin"))
async def admin_panel(message: Message, state):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Нет доступа.")
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=key)] for key in texts.keys()],
        resize_keyboard=True
    )
    await message.answer("Выберите текст для изменения:", reply_markup=kb)
    await state.set_state("admin_edit_text")

@router.message(StateFilter("admin_edit_text"))
async def admin_choose_text(message: Message, state):
    if message.text not in texts:
        await message.answer("Нет такого текста. Попробуйте снова.")
        return
    await state.update_data(edit_key=message.text)
    await message.answer(f"Текущий текст:\n{texts[message.text]}\n\nОтправьте новый текст:")
    await state.set_state("admin_edit_value")

@router.message(StateFilter("admin_edit_value"))
async def admin_set_text(message: Message, state):
    data = await state.get_data()
    key = data.get("edit_key")
    texts[key] = message.text
    save_texts(texts)
    await message.answer("Текст обновлен!", reply_markup=None)
    await state.clear()
