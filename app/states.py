from aiogram.fsm.state import State, StatesGroup

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

# Добавляем состояния для админ-панели
class AdminStates(StatesGroup):
    choosing_service = State()
    choosing_field = State()
    entering_value = State()