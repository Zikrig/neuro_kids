import os
import logging
from typing import Any, Dict
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Данные для услуг
SERVICES = {
    "neuro_diagnostic": "Нейродиагностика - 5000 руб.",
    "neuro_psychologist": "Занятия с нейропсихологом - 4000 руб./сессия",
    "sensory_integration": "Сенсорная интеграция - 4500 руб.",
    "speech_diagnostic": "Диагностика речевого развития - 3000 руб.",
    "logopedist": "Занятия с логопедом - 3500 руб./сессия",
    "child_psychologist": "Консультация детского психолога - 4000 руб.",
    "wechsler_test": "Тест Векслера - 6000 руб.",
    "floortime": "Флортайм - 4500 руб./сессия"
}

BRANCHES = [
    "Нахимовский проспект г.Москва",
    "Отрадное г.Москва",
    "Молодежная г.Москва",
    "Онлайн занятия"
]

class Form(StatesGroup):
    name = State()
    service = State()
    age = State()
    branch = State()

# Стартовое меню
def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="О ЦЕНТРЕ", callback_data="about")],
        [InlineKeyboardButton(text="УСЛУГИ И ЦЕНЫ", callback_data="services")],
        [InlineKeyboardButton(text="ОНЛАЙН РАЗВИТИЕ", callback_data="online")],
        [InlineKeyboardButton(text="ЗАПИСАТЬСЯ", callback_data="appointment")],
        [InlineKeyboardButton(text="ПОЛЕЗНАЯ ИНФОРМАЦИЯ", callback_data="info")],
        [InlineKeyboardButton(text="КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура услуг
def services_keyboard():
    builder = InlineKeyboardBuilder()
    for key, value in SERVICES.items():
        builder.button(text=value.split(" - ", 1)[0], callback_data=f"service_{key}")
    builder.button(text="↩️ Назад", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура филиалов
def branches_keyboard():
    builder = InlineKeyboardBuilder()
    for branch in BRANCHES:
        builder.button(text=branch, callback_data=f"branch_{BRANCHES.index(branch)}")
    builder.adjust(1)
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
    guide = FSInputFile("guide.pdf")  # Положите файл в папку с ботом
    await message.answer_document(guide)
    await message.answer(
        "Добро пожаловать в бот Центра детской нейропсихологии «Альтера Вита». В меню вы можете найти...",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "about")
async def about_center(callback: CallbackQuery):
    await callback.message.edit_text(
        "Мы - современный центр детской нейропсихологии с 10-летним опытом работы...",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите услугу:",
        reply_markup=services_keyboard()
    )

@router.callback_query(F.data.startswith("service_"))
async def service_detail(callback: CallbackQuery, state: FSMContext):
    service_key = callback.data.split("_", 1)[1]
    service_text = SERVICES[service_key]
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Записаться", callback_data=f"appoint_{service_key}")
    builder.button(text="↩️ Назад", callback_data="services")
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"{service_text}\n\nПодробное описание услуги...",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "online")
async def online_development(callback: CallbackQuery, state: FSMContext):
    await state.update_data(branch="Онлайн занятия")
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Записаться онлайн", callback_data="appoint_online")
    builder.button(text="↩️ Назад", callback_data="back_menu")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Онлайн-занятия с специалистами центра через Zoom/Skype...",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("appoint"))
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_", 1)[1]
    await state.update_data(service=data if data != "online" else "Онлайн-развитие")
    await state.set_state(Form.name)
    await callback.message.edit_text("Как вас зовут?")

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько лет ребенку?")

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.branch)
    await message.answer("Выберите филиал:", reply_markup=branches_keyboard())

@router.callback_query(Form.branch, F.data.startswith("branch_"))
async def process_branch(callback: CallbackQuery, state: FSMContext):
    branch_index = int(callback.data.split("_", 1)[1])
    await state.update_data(branch=BRANCHES[branch_index])
    await complete_appointment(callback, state)

async def complete_appointment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    # Заглушка для отправки данных
    print(f"Отправка в CRM: {data}")
    
    await callback.message.edit_text(
        f"Спасибо за заявку, {data['name']}!\n"
        f"Мы свяжемся с вами в ближайшее время\n\n"
        f"Данные для отправки:\n"
        f"Услуга: {SERVICES[data['service']]}\n"
        f"Возраст ребенка: {data['age']}\n"
        f"Филиал: {data['branch']}",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()

@router.callback_query(F.data == "info")
async def useful_info(callback: CallbackQuery):
    # Заглушка для чек-листов
    checklists = ["checklist1.pdf", "checklist2.pdf", "checklist3.pdf", "checklist4.pdf", "checklist5.pdf"]
    
    for checklist in checklists:
        await callback.message.answer_document(FSInputFile(checklist))
    
    await callback.message.answer(
        "Выберите раздел:",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):
    await callback.message.edit_text(
        "Наши контакты:\n"
        "Телефон: +7 (495) 123-45-67\n"
        "Email: info@altera-vita.ru\n"
        "Website: https://altera-vita.ru",
        reply_markup=main_menu_keyboard()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())