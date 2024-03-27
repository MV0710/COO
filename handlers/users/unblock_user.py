from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api import commands_user, commands_update

from data.config import admins, time_zone
from keyboards.default import back, start_markup, unblock_confirm
from keyboards.default.admis_keyboards import user_notfound
from loader import dp
from states import Unblocking, Starting

from datetime import datetime, timedelta


@dp.message_handler(text='/unblock', user_id=admins, state=Starting.choose)
async def f_command_unblock(message: types.Message):
    await message.answer(text='Введите user-ID', reply_markup=back)
    await Unblocking.user_id.set()


@dp.message_handler(user_id=admins, state=Unblocking.user_id)
async def f_user_id(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Назад':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        try:
            user_id = int(text)
        except:
            await message.answer(text='Введите корректный ID пользователя', reply_markup=back)
            return 0

        user = await commands_user.select_user(user_id=user_id)

        if user:
            await message.answer(text='Пользователь найден:\n'
                                      f'{(user[0]).user_name} (@{(user[0]).nickname}, {(user[0]).user_id})',
                                 reply_markup=unblock_confirm)
            await state.update_data(
                {
                    'user': user[0]
                }
            )
            await Unblocking.confirm.set()
        else:
            await message.answer(text='Нет такого пользователя', reply_markup=user_notfound)
            await Unblocking.user_notfound.set()


@dp.message_handler(user_id=admins, state=Unblocking.user_notfound)
async def f_user_notfound(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Повторить ввод':
        await message.answer(text='Введите user-ID', reply_markup=back)
        await Unblocking.user_id.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        await message.answer(text='Выберите действие из предложенных')


@dp.message_handler(user_id=admins, state=Unblocking.confirm)
async def f_user_notfound(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Разблокировать':
        await message.answer(text='Пользователь разблокирован', reply_markup=start_markup)
        user = (await state.get_data()).get('user')
        date_time = datetime.now() + timedelta(hours=time_zone)
        await commands_user.update_user(user_id=user.user_id, blocking=0, last_edit=date_time)
        await commands_update.add_update(user_id=user.user_id, old_status=user.blocking, new_status=0,
                                         admin_id=message.from_user.id,
                                         date_time=date_time)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Назад':
        await message.answer(text='Введите user-ID', reply_markup=back)
        await Unblocking.user_id.set()

    else:
        await message.answer(text='Выберите действие из предложенных', reply_markup=unblock_confirm)