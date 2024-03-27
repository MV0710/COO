from aiogram.dispatcher.filters.state import StatesGroup, State


class Position(StatesGroup):
    corpus = State()
    floor = State()
    block = State()
    room = State()
    motive = State()
    comment = State()
    confirmation = State()
