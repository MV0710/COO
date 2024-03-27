from aiogram.dispatcher.filters.state import StatesGroup, State


class Info(StatesGroup):
   confirm_status = State()
   corpus_edit_status = State()
   edit_status = State()
   block = State()
   clear_complaints = State()
   clear_confirm = State()
   inter_user = State()
   not_found_user = State()