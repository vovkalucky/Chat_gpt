from aiogram import types
from aiogram import F
import os
from aiogram import Bot
from bot.keyboards.user_keyboards import get_main_kb, get_admin_main_kb, get_about_kb
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from bot.external_services.openai_chatgpt import clear_context, update
from aiogram import filters
from bot.lexicon.lexicon_ru import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=['start']))
@router.callback_query(lambda callback_query: callback_query.data == 'back')
async def process_start_command(message: types.Message | types.CallbackQuery) -> None:
    # print(message.json())
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=LEXICON_RU['/start'], reply_markup=get_main_kb())
        await message.answer()
    else:
        # #await sql_add_commit(message)
        # if message.chat.id == int(os.getenv("ADMIN_ID")):
        #     await message.answer(text=LEXICON_RU['/start'], reply_markup=get_admin_main_kb())
        # else:
        await message.answer(text=LEXICON_RU['/start'], reply_markup=get_main_kb())


@router.message(Command(commands=['chat']))
@router.callback_query(lambda callback_query: callback_query.data == 'chat_with_gpt')
async def start_chat(message: types.Message | types.CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=LEXICON_RU['/chat'])
        await message.answer()  # чтобы пропали "часы" при отправке колбэка
    else:
        await message.answer(text=LEXICON_RU['/chat'])


@router.message(Command(commands=['cancel']))
async def context_clear(message: types.Message) -> None:
    await clear_context()
    await message.answer(text=LEXICON_RU['/cancel'])


@router.callback_query(lambda callback_query: callback_query.data == 'about')
async def process_button_about_press(callback: types.CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['/about'], reply_markup=get_about_kb())
    await callback.answer()

some_list = [7, 14, 28, 32, 32, '56']


def custom_filter(some_list) -> bool:
    sum = 0
    for i in some_list:
        if isinstance(i, int) and i % 7 == 0:
            sum += i
    if sum <= 83:
        return True
    else:
        return False


@router.message(filters.Text('Key'))
async def send_message(message: types.Message) -> None:
    await message.answer(text="Filter")
    print(custom_filter(some_list))


@router.message()
async def send_message(message: types.Message, bot: Bot) -> None:
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    answer_gpt = await update(message)
    await message.answer(answer_gpt)
