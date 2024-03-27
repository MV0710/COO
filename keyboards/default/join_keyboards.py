from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


faculty_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ФГиГНиГ'),
            KeyboardButton(text='ФРНиГМ'),
            KeyboardButton(text='ФПСиЭСТТ')
        ],
        [
            KeyboardButton(text='ФИМ'),
            KeyboardButton(text='ФХТиЭ'),
            KeyboardButton(text='ФАиВТ')
        ],
        [
            KeyboardButton(text='ФКБ ТЭК'),
            KeyboardButton(text='ФЭиУ'),
            KeyboardButton(text='ФМЭБ'),
            KeyboardButton(text='ФЮр')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

year_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4'),
            KeyboardButton(text='5')
        ],
        [
            KeyboardButton(text='1 магистратура'),
            KeyboardButton(text='2 магистратура')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)

cansel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)

yes_no_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


confirm_join_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)