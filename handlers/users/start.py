from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import admins
from keyboards.default.start import start_markup, start_testing

from states import Question, Starting

from utils.db_api import commands_user, commands_alert

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    nickname = message.from_user.username
    users = await commands_user.select_user(user_id)
    if not users:
        await message.answer(f"<b>Привет, {message.from_user.full_name}!</b>\n\n"
                             f"Это telegram-бот <i>Студенческого оперативного отряда РГУ нефти и газа (НИУ) "
                             f"имени И. М. Губкина</i>.\n\n"
                             f"Для того чтобы мы могли убедиться, что вы являетесь студентом нашего университета, "
                             f"необходимо пройти небольшое тестирование, состоящее из <u>2 вопросов</u>.\n\n"
                             f"<b>Внимание!</b>\n"
                             f"▪️Для прохождения тестирования вам будет дано <u>2 попытки</u>.\n"
                             f"▪️При хотя бы 1 неправильном ответе попытка не будет засчитана.\n"
                             f"▪️После второй неудачной попытки ваш аккаунт будет расценен как 'подозрительный', и мы "
                             f"будем вынуждены заблокировать его.\n"
                             f"▪️Для разблокировки аккаунта необходимо обратиться напрямую к руководству СОО.\n\n"
                             f"Для того чтобы начать тестирование, нажмите кнопку ниже ⬇️",
                             reply_markup=start_testing)
        await Question.q0.set()

    else:
        await commands_user.update_user_nickname(user_id, nickname)
        if user_id in admins:
            await message.answer(text='Для выбора корпуса отправьте боту /send, также с помощью /mg можно отправить сообщение студенту от лица бота', reply_markup=start_markup)
        else:
            await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await Starting.choose.set()


@dp.message_handler(state=Starting.choose)
async def f_choose(message: types.Message):
    await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)

