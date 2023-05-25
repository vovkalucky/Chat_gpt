from aiogram.filters.state import State, StatesGroup


class UseGPT(StatesGroup):
    state1_user_request = State()
