from aiogram.dispatcher.filters.state import StatesGroup, State


class Sending(StatesGroup):
    user_id = State()
    text = State()
    confirm = State()