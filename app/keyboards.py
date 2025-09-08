from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .services import SERVICES, BRANCHES, MULT_TABLE_BRANCHES

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

def services_keyboard():
    builder = InlineKeyboardBuilder()
    for key, value in SERVICES.items():
        builder.button(text=value.split(" - ", 1)[0], callback_data=f"service_{key}")
    builder.button(text="ТАБЛИЦА УМНОЖЕНИЯ ЗА 5 ДНЕЙ", callback_data="service_mult_table")
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
