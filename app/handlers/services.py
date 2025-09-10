from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import services_keyboard, branches_keyboard, main_menu_keyboard
import re
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import json
import os
from aiogram.types import FSInputFile

router = Router()

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    await callback.message.answer(
        "<b>НАШИ УСЛУГИ И ЦЕНЫ</b>",
        reply_markup=services_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("service_"))
async def service_detail(callback: CallbackQuery, state: FSMContext):
    service_key = callback.data.split("_", 1)[1]
    with open("data/service_details.json", encoding="utf-8") as f:
        data = json.load(f)
    details = data.get("service_details", {}).get(service_key)
    APPOINT_URL = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="ЗАПИСАТЬСЯ", url=APPOINT_URL))
    builder.button(text="↩️ Назад", callback_data="services")
    builder.adjust(1)
    if details and os.path.exists(details["image"]):
        await callback.message.answer_photo(
            FSInputFile(details["image"]),
            caption=f"<b>{details['title']}</b>",
            parse_mode="HTML"
        )
    await callback.message.answer(
        details["desc"] if details else "Описание услуги в разработке.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.message.delete()

@router.callback_query(F.data.startswith("appoint_"))
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    url = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"
    text = 'Для записи воспользуйтесь <a href="{}">формой</a>.'
    await callback.message.answer(text.format(url), parse_mode="HTML", reply_markup=main_menu_keyboard())
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
