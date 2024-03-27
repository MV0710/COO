from aiogram.dispatcher.filters.state import StatesGroup, State


class Question(StatesGroup):
    q0 = State()
    q1 = State()
    q2 = State()
    confirm1 = State()
    q0_repeat = State()
    q1_repeat = State()
    q2_repeat = State()
    confirm2 = State()