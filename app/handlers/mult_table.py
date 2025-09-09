from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards import main_menu_keyboard

router = Router()

@router.callback_query(F.data == "appoint_mult_table")
async def appoint_mult_table_link(callback: CallbackQuery, state: FSMContext):
    url = "https://tsentrdetskoyneyropsikhologiialteravita.s20.online/common/3/form/draw?id=1&baseColor=205EDC&borderRadius=8&css=%2F%2Fcdn.alfacrm.pro%2Flead-form%2Fform.css"
    text = 'Для записи воспользуйтесь <a href="{}">формой</a>.'
    await callback.message.answer(text.format(url), parse_mode="HTML", reply_markup=main_menu_keyboard())
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
