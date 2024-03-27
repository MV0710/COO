from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

corpus_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Бутлерова 1'),
            KeyboardButton(text='Бутлерова 3'),
            KeyboardButton(text='Бутлерова 5')
        ],
        [
            KeyboardButton(text='Академика Волгина 2/1'),
            KeyboardButton(text='Академика Волгина 2/2')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

floor_15_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4'),
            KeyboardButton(text='5')
        ],
        [
            KeyboardButton(text='6'),
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9'),
            KeyboardButton(text='10')
        ],
        [
            KeyboardButton(text='11'),
            KeyboardButton(text='12'),
            KeyboardButton(text='13'),
            KeyboardButton(text='14'),
            KeyboardButton(text='15')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)

floor_16_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4')
        ],
        [
            KeyboardButton(text='5'),
            KeyboardButton(text='6'),
            KeyboardButton(text='7'),
            KeyboardButton(text='8')
        ],
        [
            KeyboardButton(text='9'),
            KeyboardButton(text='10'),
            KeyboardButton(text='11'),
            KeyboardButton(text='12')
        ],
        [
            KeyboardButton(text='13'),
            KeyboardButton(text='14'),
            KeyboardButton(text='15'),
            KeyboardButton(text='16')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


def create_block(floor):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=floor + '01'),
                KeyboardButton(text=floor + '02'),
                KeyboardButton(text=floor + '03'),
                KeyboardButton(text=floor + '04'),
                KeyboardButton(text=floor + '05')
            ],
            [
                KeyboardButton(text=floor + '06'),
                KeyboardButton(text=floor + '07'),
                KeyboardButton(text=floor + '08'),
                KeyboardButton(text=floor + '09'),
                KeyboardButton(text=floor + '10')
            ],
            [
                KeyboardButton(text=floor + '11'),
                KeyboardButton(text=floor + '12'),
                KeyboardButton(text=floor + '13'),
                KeyboardButton(text=floor + '14'),
                KeyboardButton(text=floor + '15')
            ],
            [
                KeyboardButton(text=floor + '16'),
                KeyboardButton(text=floor + '17'),
                KeyboardButton(text=floor + '18'),
                KeyboardButton(text='Этаж')
            ],
            [
                KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена')
            ]
        ],
        resize_keyboard=True
    )
    return markup


def create_room(block):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=block + '/3'),
                KeyboardButton(text=block + '/2')
            ],
            [
                KeyboardButton(text=block)
            ],
            [
                KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена')
            ]
        ],
        resize_keyboard=True
    )
    return markup


motive_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запах табака, курительных смесей')
        ],
        [
            KeyboardButton(text='Шум')
        ],
        [
            KeyboardButton(text='Другое')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


comment_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пропустить')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


confirm_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить жалобу')
        ],
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)