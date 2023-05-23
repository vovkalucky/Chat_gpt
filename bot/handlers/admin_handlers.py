from aiogram import types
from bot.keyboards.user_keyboards import get_admin_main_kb
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router
from bot.lexicon.lexicon_ru import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
#@router.message_handler(user_id=5067473273)
@router.message(Command(commands=['start']), F.from_user.id == 5067473273)
@router.callback_query(lambda callback_query: callback_query.data == 'back')
async def process_start_command(message: types.Message | types.CallbackQuery) -> None:
    # print(message.json())
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=LEXICON_RU['/start'], reply_markup=get_admin_main_kb())
        await message.answer()
    else:
        await message.answer(text=LEXICON_RU['/start'], reply_markup=get_admin_main_kb())
