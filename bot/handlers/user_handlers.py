from aiogram import types
import os
from bot.keyboards.user_keyboards import get_main_kb, get_about_kb
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from bot.external_services.openai_chatgpt import clear_context, update
from aiogram import filters

# Инициализируем роутер уровня модуля
router: Router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=['start']))
@router.callback_query(lambda callback_query: callback_query.data == 'back')
async def process_start_command(message: types.Message | types.CallbackQuery) -> None:
    #print(message.json())
    text = 'Привет!\nЯ бот, демонстрирующий как работает ChatGpt. Основные команды для работы с ботом:\n\n/chat - запуск чата с нейросетью\n/cancel - сброс контекста диалога'

    if isinstance(message, CallbackQuery):
        await message.message.answer(text=text, reply_markup=get_main_kb()) #keyboard.as_markup()
        await message.answer()
    else:
        await message.answer(text=text, reply_markup=get_main_kb())



@router.message(Command(commands=['chat']))
@router.callback_query(lambda callback_query: callback_query.data == 'chat_with_gpt')
async def start_chat(message: types.Message | types.CallbackQuery) -> None:
    text = 'Введите запрос ⬇'
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=text)
        await message.answer() # чтобы пропали "часы" при отправке колбэка
    else:
        await message.answer(text=text)

@router.message(Command(commands=['cancel']))
async def context_clear(message: types.Message) -> None:
    await clear_context()
    await message.answer(text="Контекст беседы очищен.\nБот забыл предыдущий диалог")


@router.callback_query(lambda callback_query: callback_query.data == 'about')
async def process_button_about_press(callback: types.CallbackQuery):
    await callback.message.answer(text='Добавить описание', reply_markup=get_about_kb())
    await callback.answer()

some_list = [7, 14, 28, 32, 32, '56']
def custom_filter(some_list) -> bool:
    sum = 0
    for i in some_list:
        if isinstance(i, int) and i % 7 == 0:
            sum+= i
    if sum <= 83:
        return True
    else:
        return False

@router.message(filters.Text('Key'))
async def send_message(message: types.Message) -> None:
    await message.answer(text="Filter")
    print(custom_filter(some_list))


@router.message()
async def send_message(message: types.Message) -> None:
    answer_gpt = await update(message)
    await message.answer(answer_gpt)