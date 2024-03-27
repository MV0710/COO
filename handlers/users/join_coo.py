from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import faculty_markup, start_markup, year_markup, cansel_markup, yes_no_markup, \
    confirm_join_markup

from loader import dp, bot
from states import Starting, Joining
from utils.db_api import commands_user


@dp.message_handler(text='Вступить в СОО', state=Starting.choose)
async def f_join_coo(message: types.Message):
    user_id = message.from_user.id
    user = (await commands_user.select_user(user_id))[0]
    if user.blocking == 2:
        await message.answer(text='Вы не прошли регистрацию. Обратитесь к руководству СОО.')
    elif user.blocking == 1:
        await message.answer(
            text='Вы были заподозрены в подаче фейковых жалоб. Для разблокировки аккаута обратитесь к руководству СОО.')
    else:
        await message.answer(text='Укажите свой факультет', reply_markup=faculty_markup)
        await Joining.faculty.set()


@dp.message_handler(state=Joining.faculty)
async def f_faculty(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text in ['ФГиГНиГ', 'ФРНиГМ', 'ФПСиЭСТТ', 'ФИМ', 'ФХТиЭ', 'ФАиВТ', 'ФКБ ТЭК', 'ФЭиУ', 'ФМЭБ', 'ФЮр']:
        async with state.proxy() as data:
            data['faculty'] = text
        await message.answer(text='Укажите курс обучения', reply_markup=year_markup)
        await Joining.year.set()

    else:
        await message.answer(text='Выберите факультет из предложенных ⬇️', reply_markup=faculty_markup)


@dp.message_handler(state=Joining.year)
async def f_year(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Укажите свой факультет', reply_markup=faculty_markup)
        await Joining.faculty.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text in ['1', '2', '3', '4', '5', '1 магистратура', '2 магистратура']:
        async with state.proxy() as data:
            data['year'] = text
        await message.answer(text='Напишите ваш средний балл на текущий момент обучения',
                             reply_markup=cansel_markup)
        await Joining.score.set()

    else:
        await message.answer(text='Выберите год обучения из предложенных ⬇️', reply_markup=year_markup)


@dp.message_handler(state=Joining.score)
async def f_score(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Укажите курс обучения', reply_markup=year_markup)
        await Joining.year.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        async with state.proxy() as data:
            data['score'] = text
        await message.answer(text='Проживаете ли вы в общежитии?', reply_markup=yes_no_markup)
        await Joining.living.set()


@dp.message_handler(state=Joining.living)
async def f_living(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Напишите ваш средний балл на текущий момент обучения',
                             reply_markup=cansel_markup)
        await Joining.score.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text in ['Да', 'Нет']:
        async with state.proxy() as data:
            data['living'] = text
        await message.answer(text='Ваше гражданство РФ?', reply_markup=yes_no_markup)
        await Joining.nationality.set()

    else:
        await message.answer(text="Выберите 'Да' или 'Нет' ⬇️", reply_markup=yes_no_markup)


@dp.message_handler(state=Joining.nationality)
async def f_nationality(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Проживаете ли вы в общежитии?',
                             reply_markup=yes_no_markup)
        await Joining.living.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text in ['Да', 'Нет']:
        async with state.proxy() as data:
            data['nationality'] = text
        await message.answer(text='Вставьте вашу ссылку VK', reply_markup=cansel_markup)
        await Joining.link.set()

    else:
        await message.answer(text="Выберите 'Да' или 'Нет' ⬇️", reply_markup=yes_no_markup)


@dp.message_handler(state=Joining.link)
async def f_link(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Ваше гражданство РФ?', reply_markup=yes_no_markup)
        await Joining.nationality.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        async with state.proxy() as data:
            data['link'] = text

        data = await state.get_data()

        await message.answer(text='Проверьте введеные данные:\n\n'
                                  f"<i>Факультет:</i> <b>{data.get('faculty')}</b>\n"
                                  f"<i>Курс обучения:</i> <b>{data.get('year')}</b>\n"
                                  f"<i>Средний балл:</i> <b>{data.get('score')}</b>\n"
                                  f"<i>Проживаете ли в общежитии:</i> <b>{data.get('living')}</b>\n"
                                  f"<i>Гражданство РФ:</i> <b>{data.get('nationality')}</b>\n"
                                  f"<i>Ссылка на VK:</i> <b>{data.get('link')}</b>",
                             reply_markup=confirm_join_markup)
        await Joining.confirm.set()


@dp.message_handler(state=Joining.confirm)
async def f_confirm(message: types.Message, state: FSMContext):
    text = message.text
    name = message.from_user.full_name
    user_id = message.from_user.id
    nickname = message.from_user.username

    if text == 'Назад':
        await message.answer(text='Вставьте вашу ссылку VK', reply_markup=cansel_markup)
        await Joining.link.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Отправить':
        await message.answer('Заявка отправлена и в ближайшее время будет рассмотрена командиром СОО',
                             reply_markup=start_markup)

        data = await state.get_data()
        try:
            await bot.send_message(chat_id=487868221,
                                   text='Заявка на вступление\n\n'
                                        f"User-ID: <code>{user_id}</code>\n"
                                        f"User-name: {name} (@{nickname})\n"
                                        f"Факультет: {data.get('faculty')}\n"
                                        f"Курс обучения: {data.get('year')}\n"
                                        f"Средний балл: {data.get('score')}\n"
                                        f"Проживает ли в общежитии: {data.get('living')}\n"
                                        f"Гражданство РФ: {data.get('nationality')}\n"
                                        f"Ссылка на VK: {data.get('link')}")
            await bot.send_message(chat_id=586619481,
                                   text='Заявка на вступление\n\n'
                                        f"User-ID: <code>{user_id}</code>\n"
                                        f"User-name: {name} (@{nickname})\n"
                                        f"Факультет: {data.get('faculty')}\n"
                                        f"Курс обучения: {data.get('year')}\n"
                                        f"Средний балл: {data.get('score')}\n"
                                        f"Проживает ли в общежитии: {data.get('living')}\n"
                                        f"Гражданство РФ: {data.get('nationality')}\n"
                                        f"Ссылка на VK: {data.get('link')}")
        except:
            await bot.send_message(chat_id=586619481,
                                   text='Заявка на вступление\n\n'
                                        f"User-ID: <code>{user_id}</code>\n"
                                        f"User-name: {name} (@{nickname})\n"
                                        f"Факультет: {data.get('faculty')}\n"
                                        f"Курс обучения: {data.get('year')}\n"
                                        f"Средний балл: {data.get('score')}\n"
                                        f"Проживает ли в общежитии: {data.get('living')}\n"
                                        f"Гражданство РФ: {data.get('nationality')}\n"
                                        f"Ссылка на VK: {data.get('link')}")

        await state.finish()
        await Starting.choose.set()
    else:
        await message.answer('Выберите один из вариантов ⬇️', reply_markup=confirm_join_markup)

