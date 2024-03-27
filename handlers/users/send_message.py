from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from utils.db_api import commands_complaint, commands_user, commands_mg

from keyboards.default import back_markup, start_markup, cansel_markup, confirm_join_markup

from data.config import admins, time_zone, super_admins
from loader import dp, bot
from states import Starting, Sending


@dp.message_handler(Command('mg'), user_id=super_admins, state=Starting.choose)
async def start_mg_f(message: types.Message):
    await message.answer(text='Введите ID пользователя, которому хотите отправить сообщение', reply_markup=back_markup)
    await Sending.user_id.set()


@dp.message_handler(user_id=super_admins, state=Sending.user_id)
async def user_id_f(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await Starting.choose.set()

    else:
        try:
            user_id = int(text)
        except:
            await message.answer(text='Введите корректный ID пользователя')
        else:
            user = await commands_user.select_user(user_id)

            if not user:
                await message.answer(text='Нет такого пользователя\n'
                                          'Повторите попытку', reply_markup=back_markup)
            else:
                complaint = await commands_complaint.select_complaints_user((user[0]).user_id)
                answer_text = f"Ответы на <u>последнюю</u> жалобу пользователя\n" \
                              f"<b>{(user[0]).user_name}</b> (@{(user[0]).nickname}, {(user[0]).user_id}):\n\n"

                if complaint:
                    mg = await commands_mg.select_mg((complaint[0]).id)
                    admin_list = []
                    for n, m in enumerate(mg):
                        admin = (await commands_user.select_user(m.admin_id))[0]
                        answer_text += f"<b>{n+1}. Админ</b>: @{admin.nickname}\n" \
                                       f"<b>Дата:</b> {m.date_time.date()}\n" \
                                       f"<b>Время:</b> {m.date_time.time().strftime('%H:%M:%S')}\n" \
                                       f"<b>Сообщение:</b>\n" \
                                       f"<i>{m.mg}</i>\n\n"
                        admin_list.append(admin)
                    await message.answer(text=answer_text + 'Введите текст сообщения', reply_markup=cansel_markup)

                    await state.update_data(
                        {
                            'complaint': complaint,
                            'mg': mg,
                            'user': user[0],
                            'admins': admin_list,
                            'answer_text': answer_text
                        }
                    )

                else:
                    await message.answer(text=answer_text + 'Введите текст сообщения', reply_markup=cansel_markup)
                    await state.update_data(
                        {
                            'complaint': [],
                            'mg': [],
                            'user': user[0],
                            'answer_text': answer_text
                        }
                    )

                await Sending.text.set()


@dp.message_handler(user_id=super_admins, state=Sending.text)
async def text_f(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Назад':
        await message.answer(text='Введите ID пользователя, которому хотите отправить сообщение',
                             reply_markup=back_markup)
        await Sending.user_id.set()

    else:
        user = (await state.get_data()).get('user')

        await message.answer(text="Подтвердите отправку:\n\n"
                                  f"<b>Пользователь:</b>\n"
                                  f"{user.user_name} (@{user.nickname}, {user.user_id})\n\n"
                                  f"<b>Сообщение:</b>\n"
                                  f"<i>{text}</i>", reply_markup=confirm_join_markup)
        async with state.proxy() as data:
            data['text'] = text
        await Sending.confirm.set()


@dp.message_handler(user_id=super_admins, state=Sending.confirm)
async def confirm_f(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Назад':
        answer_text = (await state.get_data()).get('answer_text')
        await message.answer(text=answer_text + 'Введите текст сообщения', reply_markup=cansel_markup)

        await Sending.text.set()

    elif text == 'Отправить':
        admin_id = message.from_user.id
        data = await state.get_data()
        user = data.get('user')
        complaint = data.get('complaint')
        date_time = datetime.now() + timedelta(hours=time_zone)
        text = data.get('text')

        if complaint:
            complaint_id = (complaint[0]).id
        else:
            complaint_id = None

        try:
            await bot.send_message(chat_id=user.user_id, text='Сообщение от администратора:\n\n<i>'+text+'</i>')
        except:
            await message.answer(text='Пользователь остановил бота')
        else:
            await commands_mg.add_mg(admin_id, complaint_id, date_time, text)
            await message.answer(text='Сообщение отправлено', reply_markup=start_markup)

        await state.finish()
        await Starting.choose.set()

    else:
        await message.answer('Выберите действие из предложенных', reply_markup=confirm_join_markup)


