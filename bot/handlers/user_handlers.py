from aiogram import types
from aiogram import F
import os
from aiogram import Bot
from bot.keyboards.user_keyboards import get_main_kb, get_admin_main_kb, get_about_kb, get_examples_kb
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from bot.external_services.openai_chatgpt import clear_context, update
from aiogram import filters
from bot.lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.context import FSMContext
from bot.states.states import UseGPT

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=['start']))
@router.callback_query(lambda callback_query: callback_query.data == 'back')
async def process_start_command(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    # print(message.json())
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=LEXICON_RU['/start'], reply_markup=get_main_kb())
        await message.answer()
    else:
        await message.answer(text=LEXICON_RU['/start'], reply_markup=get_main_kb())
        #await message.edit_text(text=LEXICON_RU['/start'], reply_markup=get_main_kb())
    await state.clear()


@router.message(Command(commands=['chat']))
@router.callback_query(lambda callback_query: callback_query.data == 'chat_with_gpt')
async def start_chat(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=LEXICON_RU['/chat'])
        await message.answer()  # чтобы пропали "часы" при отправке колбэка
    else:
        await message.answer(text=LEXICON_RU['/chat'])
    await state.set_state(UseGPT.state1_user_request)


@router.message(Command(commands=['cancel']), UseGPT.state1_user_request)
async def context_clear(message: types.Message, state: FSMContext) -> None:
    await clear_context()
    await state.clear()
    await message.answer(text=LEXICON_RU['/cancel'])


@router.message(Command(commands=['cancel']))
async def context_clear(message: types.Message) -> None:
    await message.answer(text=LEXICON_RU['/cancel_error'])


@router.callback_query(lambda callback_query: callback_query.data == 'about')
async def process_button_about_press(callback: types.CallbackQuery):
    #await callback.message.delete()
    await callback.message.edit_text(text=LEXICON_RU['/about'], reply_markup=get_about_kb())
    #await callback.message.answer(text=LEXICON_RU['/about'], reply_markup=get_about_kb())
    #await callback.answer()


@router.callback_query(lambda callback_query: callback_query.data == 'examples')
async def process_button_examples_press(callback: types.CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['examples_text'], reply_markup=get_examples_kb())


@router.callback_query(lambda callback_query: callback_query.data == 'film_emodsi')
async def process_button_film_emodsi_press(callback: types.CallbackQuery):
    # Используйте свои учетные данные для авторизации в Google Sheets
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    # Получите данные с вашего листа Google Sheets
    sheet = client.open_by_key("1WjBf1DxZBX69i2VTmTvFePLNTOQZ2jJzsafGaBG_XpA").sheet1
    films_data = sheet.get_all_values()

    # Преобразуйте данные в список словарей для удобства работы
    films = []
    for row in films_data[1:]:
        film = {"id": row[1], "title_ru": row[2], "title_en": row[3], "year": int(row[4])}
        if film["year"] >= 1994:
            films.append(film)
    random_films = random.sample(films, 1)
    text = 'Вот некоторые фильмы:\n'
    for film in random_films:
        text += f"{film['title_ru']} ({film['title_en']}) - {film['year']}\n"
    await callback.message.answer(text)


@router.message(UseGPT.state1_user_request)
async def send_message(message: types.Message, bot: Bot) -> None:
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    answer_gpt = await update(message)
    await message.answer(answer_gpt)
