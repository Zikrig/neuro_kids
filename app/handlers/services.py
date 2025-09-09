from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import services_keyboard, branches_keyboard, main_menu_keyboard
from app.services import SERVICE_DETAILS, BRANCHES
from app.states import Form
import re
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

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
    details = SERVICE_DETAILS.get(service_key)
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="ЗАПИСАТЬСЯ", callback_data=f"appoint_{service_key}")
    builder.button(text="↩️ Назад", callback_data="services")
    builder.adjust(1)
    import os
    from aiogram.types import FSInputFile
    if details:
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
    else:
        await callback.message.answer(
            "Описание услуги в разработке.",
            reply_markup=builder.as_markup()
        )
    await callback.message.delete()

@router.callback_query(F.data.startswith("appoint_"))
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Для записи, пожалуйста, перейдите по ссылке:\n"
        "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css",
        disable_web_page_preview=False
    )

@router.callback_query(F.data == "appointment")
async def appointment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Для записи, пожалуйста, перейдите по ссылке:\n"
        "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css",
        disable_web_page_preview=False
    )
