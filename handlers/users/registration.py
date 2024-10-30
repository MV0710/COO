from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import time_zone
from utils.db_api import commands_user

from keyboards.default import start_markup, start_testing, confirm_answers, back_markup
from loader import dp
from states import Question, Starting

from datetime import datetime, timedelta


@dp.message_handler(state=Question.q0)
async def q0(message: types.Message):
    text = message.text
    if text == 'Начать':
        await message.answer(text='<b>Попытка 1</b>\n\n'
                                  '<i>Вопрос 1.</i>\n'
                                  '<u>Сколько цифр выделено желтым цветом в электронном пропуске студента?</u>',
                             reply_markup=ReplyKeyboardRemove())
        await Question.q1.set()
    else:
        await message.answer(text='Нажмите кнопку ниже ⬇️', reply_markup=start_testing)


@dp.message_handler(state=Question.q1)
async def q1(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['q1'] = answer
    await message.answer(text='<b>Попытка 1</b>\n\n'
                              '<i>Вопрос 2.</i>\n'
                              '<u>Сколько этажей в корпусе твоего общежития?</u>',
                         reply_markup=back_markup)
    await Question.q2.set()


@dp.message_handler(state=Question.q2)
async def q2(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='<b>Попытка 1</b>\n\n'
                                  '<i>Вопрос 1.</i>\n'
                                  '<u>Сколько цифр выделено желтым цветом в электронном пропуске студента?</u>',
                             reply_markup=ReplyKeyboardRemove())
        await Question.q1.set()

    else:
        answer1 = (await state.get_data()).get('q1')

        async with state.proxy() as data:
            data['q2'] = text

        await message.answer(text='Пожалуйста, внимательно проверьте свои ответы:\n\n'
                                  f'<i>Вопрос 1:</i> <b>{answer1}</b>\n'
                                  f'<i>Вопрос 2:</i> <b>{text}</b>',
                             reply_markup=confirm_answers)
        await Question.confirm1.set()


@dp.message_handler(state=Question.confirm1)
async def confirm_1(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Подтвердить':
        data = await state.get_data()
        answer1 = data.get('q1')
        answer2 = data.get('q2')

        if answer1 == '6' and answer2 in ['15', '16']:
            await message.answer(text='Вы успешно зарегистрированы!', reply_markup=start_markup)
            await state.finish()
            await Starting.choose.set()
            date_time = datetime.now() + timedelta(hours=time_zone)
            await commands_user.add_user(message.from_user.id, message.from_user.full_name,
                                         date_time, 0, date_time, message.from_user.username)
        else:
            await message.answer(text='<b>Вы допустили ошибку</b>\n\n'
                                      'У вас есть еще одна попытка.\n'
                                      'Для того чтобы начать тестирование, нажмите кнопку ниже ⬇️',
                                 reply_markup=start_testing)
            await Question.q0_repeat.set()

    elif text == 'Назад':
        await message.answer(text='<b>Попытка 1</b>\n\n'
                                  '<i>Вопрос 2.</i>\n'
                                  '<u>Сколько этажей в корпусе твоего общежития?</u>',
                             reply_markup=back_markup)
        await Question.q2.set()

    else:
        await message.answer(text='Нажмите на одну из предложенных кнопок ⬇️')


@dp.message_handler(state=Question.q0_repeat)
async def q0_repeat(message: types.Message):
    text = message.text
    if text == 'Начать':
        await message.answer(text='<b>Попытка 2</b>\n\n'
                                  '<i>Вопрос 1.</i>\n'
                                  '<u>Сколько цифр выделено желтым цветом в электронном пропуске студента?</u>',
                             reply_markup=ReplyKeyboardRemove())
        await Question.q1_repeat.set()
    else:
        await message.answer(text='Нажмите кнопку ниже ⬇️', reply_markup=start_testing)


@dp.message_handler(state=Question.q1_repeat)
async def q1_repeat(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['q1'] = answer
    await message.answer(text='<b>Попытка 2</b>\n\n'
                              '<i>Вопрос 2.</i>\n'
                              '<u>Сколько этажей в корпусе твоего общежития?</u>',
                         reply_markup=back_markup)
    await Question.q2_repeat.set()


@dp.message_handler(state=Question.q2_repeat)
async def q2_repeat(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='<b>Попытка 2</b>\n\n'
                                  '<i>Вопрос 1.</i>\n'
                                  '<u>Сколько цифр выделено желтым цветом в электронном пропуске студента?</u>',
                             reply_markup=ReplyKeyboardRemove())
        await Question.q1_repeat.set()

    else:
        answer1 = (await state.get_data()).get('q1')

        async with state.proxy() as data:
            data['q2'] = text

        await message.answer(text='Пожалуйста, внимательно проверьте свои ответы:\n\n'
                                  f'<i>Вопрос 1:</i> <b>{answer1}</b>\n'
                                  f'<i>Вопрос 2:</i> <b>{text}</b>',
                             reply_markup=confirm_answers)
        await Question.confirm2.set()


@dp.message_handler(state=Question.confirm2)
async def confirm_2(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Подтвердить':
        data = await state.get_data()
        answer1 = data.get('q1')
        answer2 = data.get('q2')
        date_time = datetime.now() + timedelta(hours=time_zone)

        if answer1 == '6' and answer2 in ['15', '16']:
            await message.answer(text='Вы успешно зарегистрированы!', reply_markup=start_markup)
            await commands_user.add_user(message.from_user.id, message.from_user.full_name,
                                         date_time, 0, date_time, message.from_user.username)
        else:
            await message.answer(text='<b>Вы допустили ошибку</b>\n\n'
                                      'Мы вынуждены заблокировать ваш аккаунт.\n'
                                      'Для разблокировки аккаунта обратитесь к руководству СОО.',
                                 reply_markup=start_markup)
            await commands_user.add_user(message.from_user.id, message.from_user.full_name,
                                         date_time, 2, date_time, message.from_user.username)

        await state.finish()
        await Starting.choose.set()

    elif text == 'Назад':
        await message.answer(text='<b>Попытка 2</b>\n\n'
                                  '<i>Вопрос 2.</i>\n'
                                  '<u>Сколько этажей в корпусе твоего общежития?</u>',
                             reply_markup=back_markup)
        await Question.q2_repeat.set()

    else:
        await message.answer(text='Нажмите на одну из предложенных кнопок ⬇️')