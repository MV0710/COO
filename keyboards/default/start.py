from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подать жалобу')
        ],
        [
            KeyboardButton(text='Правила пользования'),
            KeyboardButton(text='Контакты')
        ],
        [
            KeyboardButton(text='Документация'),
            KeyboardButton(text='Вступить в СОО')
        ]
    ],
    resize_keyboard=True
)

start_testing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать')
        ]
    ],
    resize_keyboard=True
)

confirm_answers = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить'),
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)