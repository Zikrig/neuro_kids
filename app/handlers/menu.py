from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from app.keyboards import main_menu_keyboard
import os
import json
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

ADMIN_ID = 184374602  # Замените на свой Telegram user_id

router = Router()

def load_texts():
    with open("data/texts.json", encoding="utf-8") as f:
        return json.load(f)

def save_texts(texts):
    with open("data/texts.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

texts = load_texts()

@router.callback_query('start')
async def after_start(callback: CallbackQuery):
    if os.path.exists("data/image10.png"):
        await callback.message.answer_photo(
            FSInputFile("data/image10.png"),
            caption=texts["greeting"],
            reply_markup=main_menu_keyboard()
        )
        return
    await callback.message.answer(
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

@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["main_menu"],
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "about")
async def about_center(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["about"],
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["contacts"],
        reply_markup=main_menu_keyboard()
    )

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

@router.message(lambda m, s: s.state == "admin_edit_text")
async def admin_choose_text(message: Message, state):
    if message.text not in texts:
        await message.answer("Нет такого текста. Попробуйте снова.")
        return
    await state.update_data(edit_key=message.text)
    await message.answer(f"Текущий текст:\n{texts[message.text]}\n\nОтправьте новый текст:")
    await state.set_state("admin_edit_value")

@router.message(lambda m, s: s.state == "admin_edit_value")
async def admin_set_text(message: Message, state):
    data = await state.get_data()
    key = data.get("edit_key")
    texts[key] = message.text
    save_texts(texts)
    await message.answer("Текст обновлен!", reply_markup=None)
    await state.clear()
