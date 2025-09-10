from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .services import SERVICES, BRANCHES, MULT_TABLE_BRANCHES

APPOINT_URL = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"

def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="ПОЛУЧИТЬ ГАЙД ПО РАЗВИТИЮ РЕБЕНКА", callback_data="get_guide")],
        [InlineKeyboardButton(text="НАШИ УСЛУГИ И ЦЕНЫ", callback_data="services")],
        [InlineKeyboardButton(text="ОНЛАЙН РАЗВИТИЕ", callback_data="online")],
        [InlineKeyboardButton(text="ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ЗАНЯТИЙ", callback_data="service_mult_table")],
        [InlineKeyboardButton(text="ЗАПИСАТЬСЯ НА КОНСУЛЬТАЦИЮ", url=APPOINT_URL)],
        [InlineKeyboardButton(text="КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def services_keyboard():
    builder = InlineKeyboardBuilder()
    for key, value in SERVICES.items():
        # Исключаем онлайн и таблицу умножения из списка услуг для пользователей
        if key in ["online", "mult_table"]:
            continue
        builder.button(text='✅' + value.split(" - ", 1)[0].upper(), callback_data=f"service_{key}")
    builder.button(text="↩️ Назад", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()

def branches_keyboard():
    builder = InlineKeyboardBuilder()
    for branch in BRANCHES:
        builder.button(text=branch, callback_data=f"branch_{BRANCHES.index(branch)}")
    builder.adjust(1)
    return builder.as_markup()

def mult_table_branches_keyboard():
    builder = InlineKeyboardBuilder()
    for branch in MULT_TABLE_BRANCHES:
        builder.button(text=branch, callback_data=f"mult_branch_{MULT_TABLE_BRANCHES.index(branch)}")
    builder.adjust(1)
    return builder.as_markup()
