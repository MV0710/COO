from aiogram.dispatcher.filters.state import StatesGroup, State


class Starting(StatesGroup):
    choose = State()