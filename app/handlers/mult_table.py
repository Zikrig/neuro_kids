from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import mult_table_branches_keyboard, main_menu_keyboard
from app.services import MULT_TABLE_BRANCHES
from app.states import MultTableForm

router = Router()

@router.callback_query(F.data == "appoint_mult_table")
async def start_mult_table_appointment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MultTableForm.name)
    await callback.message.answer("Ваше имя:")

@router.message(MultTableForm.name)
async def mult_table_name(message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(MultTableForm.phone)
    await message.answer("Ваш контактный телефон:")

@router.message(MultTableForm.phone)
async def mult_table_phone(message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(MultTableForm.age)
    await message.answer("Возраст ребенка (полных лет):")

@router.message(MultTableForm.age)
async def mult_table_age(message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(MultTableForm.branch)
    await message.answer("Выберите удобный филиал в г. Москва:", reply_markup=mult_table_branches_keyboard())

@router.callback_query(MultTableForm.branch, F.data.startswith("mult_branch_"))
async def mult_table_branch(callback: CallbackQuery, state: FSMContext):
    branch_index = int(callback.data.split("_", 2)[2])
    await state.update_data(branch=MULT_TABLE_BRANCHES[branch_index])
    await complete_mult_table_appointment(callback, state)

async def complete_mult_table_appointment(callback: CallbackQuery, state: FSMContext):
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
