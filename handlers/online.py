from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_keyboard
from services import ONLINE_DETAILS
import os

router = Router()

@router.callback_query(F.data == "online")
async def online_development(callback: CallbackQuery, state: FSMContext):
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="ЗАПИСАТЬСЯ", callback_data="appoint_online")
    builder.button(text="↩️ Назад", callback_data="back_menu")
    builder.adjust(1)
    details = ONLINE_DETAILS
    if os.path.exists(details["image"]):
        await callback.message.answer_photo(
            FSInputFile(details["image"]),
            caption=f"<b>{details['title']}</b>",
            parse_mode="HTML"
        )
    await callback.message.answer(
        details["desc"],
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.message.delete()
