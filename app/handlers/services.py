from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import services_keyboard, branches_keyboard, main_menu_keyboard
from app.services import SERVICE_DETAILS, BRANCHES
from app.states import Form

router = Router()

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>НАШИ УСЛУГИ И ЦЕНЫ</b>\n\nВыберите услугу:",
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

@router.callback_query(F.data.startswith("appoint"))
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_", 1)[1]
    await state.update_data(service=data)
    await state.set_state(Form.name)
    await callback.message.edit_text("Ваше имя:")

@router.message(Form.name)
async def process_name(message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)
    await message.answer("Ваш контактный телефон:")

@router.message(Form.phone)
async def process_phone(message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Form.age)
    await message.answer("Возраст ребенка (полных лет):")

@router.message(Form.age)
async def process_age(message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.branch)
    await message.answer("Выберите удобный филиал:", reply_markup=branches_keyboard())

@router.callback_query(Form.branch, F.data.startswith("branch_"))
async def process_branch(callback: CallbackQuery, state: FSMContext):
    branch_index = int(callback.data.split("_", 1)[1])
    await state.update_data(branch=BRANCHES[branch_index])
    await complete_appointment(callback, state)

async def complete_appointment(callback: CallbackQuery, state: FSMContext):
    from app.services import SERVICE_DETAILS
    data = await state.get_data()
    service_value = SERVICE_DETAILS.get(data.get('service'), {}).get('title', data.get('service'))
    await callback.message.edit_text(
        f"Спасибо за заявку, {data.get('name', '')}!\n"
        f"Мы свяжемся с вами в ближайшее время\n\n"
        f"Данные для отправки в CRM:\n"
        f"Услуга: {service_value}\n"
        f"Телефон: {data.get('phone', '')}\n"
        f"Возраст ребенка: {data.get('age', '')}\n"
        f"Филиал: {data.get('branch', '')}",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
