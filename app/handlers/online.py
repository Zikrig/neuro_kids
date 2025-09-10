from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import main_menu_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import json
import os
from aiogram.types import FSInputFile
from app.stats_manager import stats_manager

router = Router()

APPOINT_URL = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"

@router.callback_query(F.data == "online")
async def online_development(callback: CallbackQuery, state: FSMContext):
    stats_manager.increment("online")
    with open("data/service_details.json", encoding="utf-8") as f:
        data = json.load(f)
    details = data.get("online_details")
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="ЗАПИСАТЬСЯ", url=APPOINT_URL))
    builder.add(InlineKeyboardButton(text="↩️ Назад", callback_data="back_menu"))
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
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
