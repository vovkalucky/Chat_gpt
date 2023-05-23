from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon.lexicon_ru import LEXICON_RU

def get_main_kb() -> InlineKeyboardMarkup:
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['chat_with_gpt'],
        callback_data='chat_with_gpt')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['about'],
        callback_data='about')
    # Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2)
    keyboard.adjust(1)  # делает строки по 1 кнопке
    return keyboard.as_markup()

def get_admin_main_kb() -> InlineKeyboardMarkup:
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['chat_with_gpt'],
        callback_data='chat_with_gpt')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['about'],
        callback_data='about')
    url_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin'],
        callback_data='admin')
    # Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2).add(url_button_3)
    keyboard.adjust(1)  # делает строки по 1 кнопке
    return keyboard.as_markup()


def get_about_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['back'],
        callback_data="back")
    )
    return keyboard.as_markup()