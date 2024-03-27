from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


block_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заблокировать'),
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)


unblock_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Разблокировать'),
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)