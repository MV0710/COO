from aiogram.dispatcher.filters.state import StatesGroup, State


class Joining(StatesGroup):
    faculty = State()
    year = State()
    score = State()
    living = State()
    nationality = State()
    link = State()
    confirm = State()
