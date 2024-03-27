from aiogram.dispatcher.filters.state import StatesGroup, State


class Unblocking(StatesGroup):
    user_id = State()
    user_notfound = State()
    confirm = State()