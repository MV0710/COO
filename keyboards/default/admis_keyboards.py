from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


corpus_info = ReplyKeyboardMarkup(
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
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


info_status = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Показать текущий статус'),
            KeyboardButton(text='Изменить статус')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


confirm_status = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)


corpus_edit_status = ReplyKeyboardMarkup(
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
            KeyboardButton(text='Далее'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


edit_status = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправлять'),
            KeyboardButton(text='Не отправлять')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)


clear_complaint = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Другой блок'),
        ],
        [
            KeyboardButton(text='Обработать'),
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


clear_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить'),
            KeyboardButton(text='Назад')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)


user_notfound = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Повторить ввод')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)