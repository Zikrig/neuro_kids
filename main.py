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
    "floortime": "Флортайм - 4500 руб./сессия",
    "online": "Онлайн-развитие"
}

# Обновленный список филиалов
BRANCHES = [
    "Нахимовский проспект (Москва)",
    "Молодежная (Москва)",
    "Отрадное (Москва)",
    "ОНЛАЙН формат"
]

# Подробные описания услуг и изображения
SERVICE_DETAILS = {
    "neuro_diagnostic": {
        "title": "НЕЙРОДИАГНОСТИКА",
        "image": "data/image1.png",
        "desc": (
            "<b>Тестирование ребенка, которое позволяет определить:</b>\n"
            "уровень развития памяти, внимание, мышления, речи и др.\n"
            "сильные и слабые стороны, потенциал развития\n"
            "первопричины имеющихся трудностей\n"
            "уровень готовности к успешному школьному обучению\n\n"
            "Необходимо для составления индивидуального коррекционно-развивающего маршрута.\n\n"
            "Проводит нейропсихолог, длительность – 1 час\n"
            "<b>ОЧНО</b> (для детей от 2 до 16 лет) – 4500 руб.\n"
            "<b>ОНЛАЙН</b> (для детей от 4 лет) – 2500 руб.\n\n"
            "По итогам нейродиагностики специалист дает развернутую консультацию по дальнейшему развитию ребенка, выдает заполненную брошюру с итогами тестирования, рекомендациями и полезными материалами."
        )
    },
    "neuro_psychologist": {
        "title": "ЗАНЯТИЯ С НЕЙРОПСИХОЛОГОМ",
        "image": "data/image2.png",
        "desc": (
            "С помощью специальных физических и когнитивных упражнений специалист помогает сформировать навыки - основу для успешного обучения, поведения и общения: внимание, память, самоконтроль, речь и пространственное мышление.\n\n"
            "Занятия необходимы, если у ребёнка есть трудности с обучением (невнимательность, дислексия, дисграфия, плохая память и др.), поведением (гиперактивность, импульсивность, медлительность и др.), речью, если он неуклюж, плохо ориентируется в пространстве. Также они показаны при любых задержках развития.\n\n"
            "Проводит нейропсихолог, длительность от 40 до 55 мин.\n"
            "<b>ОЧНО</b> (для детей от 2 до 16 лет) – 3200 – 3500 руб.\n"
            "<b>ОНЛАЙН</b> (для детей от 4 лет) – 2000 руб.\n\n"
            "Для составления программы необходимо проведение нейродиагностики (можно предоставить заключение из другого центра)."
        )
    },
    "handwriting": {
        "title": "КОРРЕКЦИЯ ПОЧЕРКА",
        "image": "data/image3.png",
        "desc": (
            "Занятия по специализированной программе с нейропсихологом или логопедом, направленные на:\n"
            "развитие интереса к каллиграфии, письму\n"
            "формирование графического навыка\n"
            "развитие чувства ритма, пространственных представлений\n"
            "развитие мелкой и крупной моторики\n\n"
            "Программа занятий индивидуальна для каждого ребенка и составляется на основе данных, полученных в результате проведенной нейропсихологической диагностики (можно предоставить заключение из другого центра).\n\n"
            "<b>ОЧНО</b> – 3300 руб.\n"
            "<b>ОНЛАЙН</b> – 2000 руб."
        )
    },
    "speech_diagnostic": {
        "title": "ДИАГНОСТИКА РЕЧЕВОГО РАЗВИТИЯ",
        "image": "data/image4.png",
        "desc": (
            "Консультация логопеда или логопеда-дефектолога, в ходе которой специалист определяет уровень речевого развития ребенка, соответствие возрастным нормативам, дает развернутую консультацию родителям.\n\n"
            "По итогам тестирования специалист выдает брошюру с краткими итогами, рекомендациями и полезными материалами.\n\n"
            "Необходима, если ребенок не говорит в 2 года и старше, плохо говорит («каша» во рту, не выговаривает звуки, неправильно строит предложения и др.), не понимает обращенную речь, есть трудности освоения письма и чтения.\n\n"
            "<b>ОЧНО</b> (для детей от 2 до 16 лет) – 3400 руб.\n"
            "<b>ОНЛАЙН</b> (для детей от 3,5 лет) – 1000 руб."
        )
    },
    "logopedist": {
        "title": "ЗАНЯТИЯ С ЛОГОПЕДОМ",
        "image": "data/image5.png",
        "desc": (
            "Помогают:\n"
            "запустить речь\n"
            "исправить нарушения звукопроизношения\n"
            "развить связную речь\n"
            "обогатить словарный запас\n"
            "наладить грамматический строй речи\n"
            "улучшить фонематический слух\n"
            "преодолеть трудности освоения письма и чтения\n\n"
            "<b>ОЧНО</b> (для детей от 2 до 16 лет) – 3000 руб.\n"
            "<b>ОНЛАЙН</b> (для детей от 3,5 лет) – 1000 руб.\n\n"
            "Для составления индивидуальной программы занятий необходимо проведение логопедической диагностики (можно предоставить заключение из другого центра)"
        )
    },
    "child_psychologist": {
        "title": "КОНСУЛЬТАЦИЯ ПСИХОЛОГА",
        "image": "data/image5.png",
        "desc": (
            "Детский/подростковый психолог поможет в следующих случаях:\n"
            "поведенческие проблемы (агрессия, истерики, замкнутость)\n"
            "трудности в общении со сверстниками и взрослыми\n"
            "резкое снижении успеваемости\n"
            "повышенная тревожность, страхи\n"
            "переживание стрессовых ситуаций (развод родителей, потеря близкого, буллинг, переезд)\n\n"
            "Консультация специалиста важна и при заметных изменениях в настроении или поведении ребёнка, которые беспокоят родителей.\n\n"
            "Длительность – 55 мин, стоимость – 4500 руб. (очно или онлайн)"
        )
    },
    "wechsler_test": {
        "title": "ТЕСТ ВЕКСЛЕРА",
        "image": "data/image7.png",
        "desc": (
            "Один из самых известных и широко используемых инструментов для оценки интеллекта и когнитивных способностей у детей от 5 до 16 лет.\n\n"
            "Результаты показывают не только общий уровень интеллекта (IQ), но и сильные и слабые стороны когнитивного профиля ребёнка, что помогает выявить причины трудностей в обучении (например, дислексию, СДВГ), одарённость или задержки развития. Тест часто используется для составления индивидуальных образовательных программ.\n\n"
            "Проводит нейропсихолог, длительность 2 часа, стоимость – 6500 руб. (только ОЧНО)."
        )
    },
    "mult_table": {
        "title": "ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ДНЕЙ",
        "image": "data/image8.png",
        "desc": (
            "Традиционный метод заучивания таблицы умножения давно критикуют педагоги и нейропсихологи, ведь он основан на зазубривании, отсутствии вовлеченности, игнорировании особенностей памяти и страхе ошибок.\n\n"
            "Наша авторская программа позволяет освоить таблицу умножения всего за 5 занятий:\n"
            "без зубрежки и стресса\n"
            "через игру, а не принуждение\n"
            "с использованием мнемотехник и ассоциаций\n\n"
            "Дети играют и даже не замечают, как запоминают таблицу умножения раз и навсегда!\n\n"
            "Курс – 5 занятий по 1,5 часа\n"
            "Стоимость курса – 10000 руб.\n"
            "В филиалах <b>«Отрадное»</b> и <b>«Молодежная»</b> (г. Москва)"
        )
    }
}

ONLINE_DETAILS = {
    "title": "ОНЛАЙН РАЗВИТИЕ",
    "image": "data/image9.png",
    "desc": (
        "Мы разработали и успешно практикуем специализированные программы занятий с нейропсихологом и логопедом-дефектологом в ОНЛАЙН формате. Развитие внимания, мышления, памяти и речи стало доступным и удобным, но не менее эффективным.\n\n"
        "Сила нейрокоррекции и логопедии теперь в гармоничном цифровом пространстве!\n\n"
        "<b>Нейродиагностика</b> (для детей от 4 лет) – 2500 руб., 1-1,5 часа\n"
        "<b>Занятия с нейропсихологом</b> (для детей от 4 лет) – 2000 руб., 50 мин.\n"
        "<b>Логопедическая диагностика</b> (для детей от 3,5 лет) – 1000 руб., 45 мин.\n"
        "<b>Занятия с логопедом/логопедом-дефектологом</b> (для детей от 3,5 лет) – 1000 руб., 35 мин.\n"
        "<b>Консультация нейропсихолога</b> (беседа с родителями детей любых возрастов) – 2000 руб, 50 мин.\n"
        "<b>Консультация логопеда</b> (беседа с родителями детей любых возрастов) – 1000 руб, 50 мин."
    )
}

class Form(StatesGroup):
    name = State()
    phone = State()
    age = State()
    branch = State()

class MultTableForm(StatesGroup):
    name = State()
    phone = State()
    age = State()
    branch = State()

class OnlineForm(StatesGroup):
    name = State()
    phone = State()
    age = State()

# Стартовое меню
def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="ПОЛУЧИТЬ ГАЙД ПО РАЗВИТИЮ РЕБЕНКА", callback_data="get_guide")],
        [InlineKeyboardButton(text="НАШИ УСЛУГИ И ЦЕНЫ", callback_data="services")],
        [InlineKeyboardButton(text="ОНЛАЙН РАЗВИТИЕ", callback_data="online")],
        [InlineKeyboardButton(text="ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ЗАНЯТИЙ", callback_data="service_mult_table")],
        [InlineKeyboardButton(text="ЗАПИСАТЬСЯ НА КОНСУЛЬТАЦИЮ", callback_data="appointment")],
        [InlineKeyboardButton(text="КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура услуг
def services_keyboard():
    builder = InlineKeyboardBuilder()
    for key, value in SERVICES.items():
        builder.button(text=value.split(" - ", 1)[0], callback_data=f"service_{key}")
    builder.button(text="ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ДНЕЙ", callback_data="service_mult_table")
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

# Добавляем филиалы для курса таблицы умножения
MULT_TABLE_BRANCHES = [
    "Отрадное (Москва)",
    "Молодежная (Москва)"
]

def mult_table_branches_keyboard():
    builder = InlineKeyboardBuilder()
    for branch in MULT_TABLE_BRANCHES:
        builder.button(text=branch, callback_data=f"mult_branch_{MULT_TABLE_BRANCHES.index(branch)}")
    builder.adjust(1)
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "<b>Altera Vita Bot</b>\n\n"
        "Добро пожаловать в официальный бот Центра детской нейропсихологии «Альтера Вита» 🌺\n\n"
        "Это — безопасное пространство для родителей, которые хотят помочь ребенку раскрыть свой потенциал.\n\n"
        "Вас беспокоит речь, поведение, развитие или успехи в учебе❓\n"
        "Вы пришли по адресу 🤗\n\n"
        "💯 Наш бот поможет вам получить полезные материалы, выбрать специалиста, записаться на консультацию, узнать нас лучше, сделать первый и самый важный шаг навстречу решению.\n\n"
        "Нажмите <b>Start</b>, и мы поможем разобраться."
    )
    await message.answer(welcome_text, parse_mode="HTML")
    if os.path.exists("data/image10.png"):
        await message.answer_photo(FSInputFile("data/image10.png"))
    await message.answer(
        "<b>START</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="START", callback_data="start_menu")]]
        ),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "start_menu")
async def after_start(callback: CallbackQuery):
    await callback.message.edit_text(
        "Прекрасно! Давайте вместе разберемся в ситуации и найдем наилучший путь решения.",
        reply_markup=None
    )
    if os.path.exists("data/image10.png"):
        await callback.message.answer_photo(FSInputFile("data/image10.png"))
    await callback.message.answer(
        "Выберите раздел:",
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
        "Выберите раздел:",
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
        "<b>НАШИ УСЛУГИ И ЦЕНЫ</b>\n\nВыберите услугу:",
        reply_markup=services_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("service_"))
async def service_detail(callback: CallbackQuery, state: FSMContext):
    service_key = callback.data.split("_", 1)[1]
    details = SERVICE_DETAILS.get(service_key)
    builder = InlineKeyboardBuilder()
    builder.button(text="ЗАПИСАТЬСЯ", callback_data=f"appoint_{service_key}")
    builder.button(text="↩️ Назад", callback_data="services")
    builder.adjust(1)
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

@router.callback_query(F.data == "online")
async def online_development(callback: CallbackQuery, state: FSMContext):
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

@router.callback_query(F.data == "service_mult_table")
async def mult_table_detail(callback: CallbackQuery, state: FSMContext):
    details = SERVICE_DETAILS["mult_table"]
    builder = InlineKeyboardBuilder()
    builder.button(text="ЗАПИСАТЬСЯ", callback_data="appoint_mult_table")
    builder.button(text="↩️ Назад", callback_data="services")
    builder.adjust(1)
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

@router.callback_query(F.data.startswith("appoint"))
async def start_appointment(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_", 1)[1]
    await state.update_data(service=data)
    await state.set_state(Form.name)
    await callback.message.edit_text("Ваше имя:")

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)
    await message.answer("Ваш контактный телефон:")

@router.message(Form.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Form.age)
    await message.answer("Возраст ребенка (полных лет):")

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.branch)
    await message.answer("Выберите удобный филиал:", reply_markup=branches_keyboard())

@router.callback_query(Form.branch, F.data.startswith("branch_"))
async def process_branch(callback: CallbackQuery, state: FSMContext):
    branch_index = int(callback.data.split("_", 1)[1])
    await state.update_data(branch=BRANCHES[branch_index])
    await complete_appointment(callback, state)

async def complete_appointment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Заглушка для отправки данных
    print(f"Отправка в CRM: {data}")
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

@router.callback_query(F.data == "appoint_mult_table")
async def start_mult_table_appointment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MultTableForm.name)
    await callback.message.edit_text("Ваше имя:")

@router.message(MultTableForm.name)
async def mult_table_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(MultTableForm.phone)
    await message.answer("Ваш контактный телефон:")

@router.message(MultTableForm.phone)
async def mult_table_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(MultTableForm.age)
    await message.answer("Возраст ребенка (полных лет):")

@router.message(MultTableForm.age)
async def mult_table_age(message: Message, state: FSMContext):
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
    await callback.message.edit_text(
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

@router.callback_query(F.data == "info")
async def useful_info(callback: CallbackQuery):
    checklists = ["data/checklist1.pdf", "data/checklist2.pdf", "data/checklist3.pdf", "data/checklist4.pdf", "data/checklist5.pdf"]
    for checklist in checklists:
        if os.path.exists(checklist):
            await callback.message.answer_document(FSInputFile(checklist))
        else:
            await callback.message.answer(f"Файл {checklist} не найден.")
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