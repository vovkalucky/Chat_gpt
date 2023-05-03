from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_kb() -> InlineKeyboardMarkup:
    #Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    #Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='🧑🏻‍💻 Начать чат с ChatGPT',
        callback_data='chat_with_gpt')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='ℹ️ О боте',
        callback_data='about')
    #Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2)
    keyboard.adjust(1) # делает строки по 1 кнопке
    return keyboard.as_markup()

def get_about_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="↩️ Назад",
        callback_data="back")
    )
    return keyboard.as_markup()