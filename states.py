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
