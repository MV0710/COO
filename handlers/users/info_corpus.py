from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import admins
from loader import dp
from states import Info, Starting

from utils.misc import grouping, corpus_dict
from utils.db_api import commands_complaint

from keyboards.default import back, start_markup, clear_complaint, clear_confirm


@dp.message_handler(Command('base'), user_id=admins, state=Starting.choose)
async def get_complaints(message: types.Message):
    data = await commands_complaint.select_all_complaints()
    answer_text = ''
    for complaint in data[:min(len(data), 10)]:
        answer_text += f'{complaint.id}, {complaint.user_name}, {complaint.user_id}, ' \
                       f'{complaint.date_time.date()}, {complaint.date_time.time().strftime("%H:%M:%S")}' \
                       f', {complaint.corpus}, {complaint.floor}, {complaint.block}, {complaint.room}, ' \
                       f'{complaint.motive}, {complaint.comment[:min(len(complaint.comment), 100)]}, {complaint.status}'
        answer_text += '\n'
    await message.answer(text=answer_text)


@dp.message_handler(text=['/b1', '/b3', '/b5', '/v1', '/v2'], user_id=admins, state=Starting.choose)
async def get_b1(message: types.Message, state: FSMContext):
    text = message.text
    corpus = corpus_dict.get(text)

    data = await commands_complaint.select_complaints(corpus=corpus, status='Не обработано')
    group_data = grouping(data)
    await Info.block.set()
    await state.update_data(
        {
            'data': group_data,
            'corpus': corpus
        }
    )
    answer_text = f'Список нарушений корпуса {corpus}:\n\n'
    for key in group_data.keys():
        answer_text += f'<code>{key}</code>' + ': ' + str(len(group_data[key])) + '\n'
    await message.answer(text=answer_text, reply_markup=back)


@dp.message_handler(state=Info.block, user_id=admins)
async def get_block_b1(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()

    if text == 'Назад':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text in (data.get('data')).keys():
        async with state.proxy() as d:
            d['block'] = text
        complaints = (data.get('data')).get(text)
        if text[:4] == 'Этаж':
            answer_text = f'Список нарушений на {(complaints[0]).floor} этаже:\n\n'
            count = 1
            for complaint in complaints[:min(len(complaints), 10)]:
                if not complaint.comment:
                    comment = '_'
                else:
                    comment = complaint.comment
                answer_text += f'{count}.\n' \
                            f'Пользователь: {complaint.user_name} (@{complaint.nickname}, <code>{complaint.user_id}</code>)\n' \
                            f'Дата жалобы: {complaint.date_time.date()}\n' \
                            f'Время жалобы: {complaint.date_time.time().strftime("%H:%M:%S")}\n' \
                            f'Причина жалобы: {complaint.motive}\n' \
                            f'Комментарий: {comment[:min(len(comment), 200)]}\n\n'
                count += 1
        else:
            answer_text = f'Список нарушений на блок {(complaints[0]).block}:\n\n'
            count = 1
            for complaint in complaints[:min(len(complaints), 10)]:
                if not complaint.comment:
                    comment = '_'
                else:
                    comment = complaint.comment
                answer_text += f'{count}.\n' \
                            f'Пользователь: {complaint.user_name} (@{complaint.nickname}, <code>{complaint.user_id}</code>)\n' \
                            f'Дата жалобы: {complaint.date_time.date()}\n' \
                            f'Время жалобы: {complaint.date_time.time().strftime("%H:%M:%S")}\n' \
                            f'Комната: {complaint.room}\n' \
                            f'Причина жалобы: {complaint.motive}\n' \
                            f'Комментарий: {comment[:min(len(comment), 200)]}\n\n'
                count += 1
        await Info.clear_complaints.set()
        await message.answer(text=answer_text, reply_markup=clear_complaint)

    else:
        await message.answer(text='Укажите блок или вернитесь назад')


@dp.message_handler(state=Info.clear_complaints, user_id=admins)
async def clearing_block(message: types.Message, state: FSMContext):
    text = message.text
    corpus = (await state.get_data()).get('corpus')

    if text == 'Отмена':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Другой блок':
        data = await commands_complaint.select_complaints(corpus=corpus, status='Не обработано')
        group_data = grouping(data)

        await Info.block.set()
        await state.update_data(
            {
                'data': group_data
            }
        )
        text = f'Список нарушений корпуса {corpus}:\n\n'
        for key in group_data.keys():
            text += f'<code>{key}</code>' + ': ' + str(len(group_data[key])) + '\n'
        await message.answer(text=text, reply_markup=back)

    elif text == 'Обработать':
        await Info.clear_confirm.set()
        await message.answer(text='Подтвердите действие', reply_markup=clear_confirm)

    else:
        await message.answer(text='Выберите действия из предложенных')


@dp.message_handler(state=Info.clear_confirm, user_id=admins)
async def clearing_confirm(message: types.Message, state: FSMContext):
    text = message.text
    corpus = (await state.get_data()).get('corpus')

    if text == 'Отмена':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Назад':
        data = await commands_complaint.select_complaints(corpus=corpus, status='Не обработано')
        group_data = grouping(data)

        await Info.block.set()
        await state.update_data(
            {
                'data': group_data
            }
        )
        text = f'Список нарушений корпуса {corpus}:\n\n'
        for key in group_data.keys():
            text += f'<code>{key}</code>' + ': ' + str(len(group_data[key])) + '\n'
        await message.answer(text=text, reply_markup=back)

    elif text == 'Подтвердить':
        data = await state.get_data()
        corpus = data.get('corpus')
        block = data.get('block')

        if block[:4] == 'Этаж':
            await commands_complaint.update_complaints_floor(corpus=corpus, block='Этаж', floor=block[5:], status='Обработано')
        else:
            await commands_complaint.update_complaints(corpus=corpus, block=block, status='Обработано')

        await message.answer(text='Нарушения обработаны', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
