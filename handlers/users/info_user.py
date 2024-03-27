from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api import commands_complaint

from data.config import admins
from keyboards.default import back, start_markup
from keyboards.default.admis_keyboards import user_notfound
from loader import dp
from states import Info, Starting


@dp.message_handler(text='/user', user_id=admins, state=Starting.choose)
async def command_user(message: types.Message):
    await message.answer(text='Введите user-ID', reply_markup=back)
    await Info.inter_user.set()


@dp.message_handler(user_id=admins, state=Info.inter_user)
async def info_user(message: types.Message, state: FSMContext):
    user_id = message.text

    if user_id == 'Назад':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        try:
            user_id = int(user_id)
        except:
            await message.answer(text='Введите корректный ID пользователя', reply_markup=back)
            return 0

        data = await commands_complaint.select_complaints_user(user_id=user_id)

        if data:
            answer_text = f'Жалобы от пользователя\n' \
                          f'{(data[0]).user_name} (@{(data[0]).nickname}, {user_id}):\n\n'
            count = 1

            for complaint in data[:min(10, len(data)+1)]:
                if not complaint.comment:
                    comment = '_'
                else:
                    comment = complaint.comment
                if complaint.block == 'Этаж':
                    answer_text += f'{count}.\n' \
                                    f'Дата жалобы: {complaint.date_time.date()}\n' \
                                    f'Время жалобы: {complaint.date_time.time().strftime("%H:%M:%S")}\n' \
                                    f'Корпус: {complaint.corpus}\n' \
                                    f'Этаж: {complaint.floor}\n' \
                                    f'Причина жалобы: {complaint.motive}\n' \
                                    f'Комментарий: {comment[:min(len(comment), 200)]}\n\n'
                else:
                    answer_text += f'{count}.\n' \
                                   f'Дата жалобы: {complaint.date_time.date()}\n' \
                                   f'Время жалобы: {complaint.date_time.time().strftime("%H:%M:%S")}\n' \
                                   f'Корпус: {complaint.corpus}\n' \
                                   f'Комната: {complaint.room}\n' \
                                   f'Причина жалобы: {complaint.motive}\n' \
                                   f'Комментарий: {comment[:min(len(comment), 200)]}\n\n'
                count += 1
            await message.answer(text=answer_text, reply_markup=start_markup)
            await state.finish()
            await Starting.choose.set()

        else:
            await message.answer(text='Нет такого пользователя', reply_markup=user_notfound)
            await Info.not_found_user.set()


@dp.message_handler(user_id=admins, state=Info.not_found_user)
async def repeat_info_user(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'Повторить ввод':
        await message.answer(text='Введите user-ID', reply_markup=back)
        await Info.inter_user.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        await message.answer(text='Выберите действие из предложенных ⬇️')