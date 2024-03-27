from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins, time_zone
from keyboards.default import corpus_markup, floor_15_markup, floor_16_markup, start_markup, create_block, create_room,\
    motive_markup, comment_markup, confirm_markup
from loader import dp, bot
from states import Position, Starting

from utils.db_api import commands_complaint, commands_alert, commands_user

from datetime import datetime, timedelta


@dp.message_handler(text='Подать жалобу', state=Starting.choose)
async def enter_start(message: types.Message):
    user_id = message.from_user.id
    user = (await commands_user.select_user(user_id))[0]
    if user.blocking == 2:
        await message.answer(text='Вы не прошли регистрацию. Обратитесь к руководству СОО.')
    elif user.blocking == 1:
        await message.answer(text='Вы были заподозрены в подаче фейковых жалоб. Для разблокировки аккаута обратитесь к руководству СОО.')
    else:
        #last_complaints = await commands_complaint.select_complaints_user(user_id=user_id)
        #if last_complaints:
            #if datetime.now() + timedelta(hours=time_zone) < last_complaints[0].date_time + timedelta(minutes=30):
                #await message.answer(text='Жалобы можно отправлять не чаще 1 раза в 30 минут.\n'
                                          #'Пожалуйста, подождите.')
                #return 0

        await message.answer(text='Укажите корпус, в котором замечено нарушение', reply_markup=corpus_markup)
        await Position.corpus.set()


@dp.message_handler(state=Position.corpus)
async def enter_corpus(message: types.Message, state: FSMContext):
    text = message.text
    if text == 'Назад':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif text in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5']:
        await message.answer(text='Укажите этаж', reply_markup=floor_15_markup)
        await Position.floor.set()
        async with state.proxy() as data:
            data['Corpus'] = text
    elif text in ['Академика Волгина 2/1', 'Академика Волгина 2/2']:
        await message.answer(text='Укажите этаж', reply_markup=floor_16_markup)
        await Position.floor.set()
        async with state.proxy() as data:
            data['Corpus'] = text
    else:
        await message.answer(text='Введите корпус из данного списка:\n\n'
                                  '▪️Бутлерова 1\n'
                                  '▪️Бутлерова 3\n'
                                  '▪️Бутлерова 5\n'
                                  '▪️Академика Волгина 2/1\n'
                                  '▪️Академика Волгина 2/2')


@dp.message_handler(state=Position.floor)
async def enter_floor(message: types.Message, state: FSMContext):
    text = message.text
    position = await state.get_data()
    if text == 'Назад':
        await message.answer(text='Укажите корпус, в котором замечено нарушение', reply_markup=corpus_markup)
        await Position.previous()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif position.get('Corpus') in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5']:
        if text in ['1', '2', '3', '4', '5',
                    '6', '7', '8', '9', '10',
                    '11', '12', '13', '14', '15']:
            await message.answer(text="Укажите блок\n\n"
                                      "Если нарушение происходит не в блоке (в коридоре, на кухне, на лестничной"
                                      " площадке), или вы не знаете точно где, выберете 'Этаж' и "
                                      "в комментарии уточните информацию",
                                 reply_markup=create_block(text))
            await Position.block.set()
            async with state.proxy() as data:
                data['Floor'] = text
        else:
            await message.answer(text='Укажите существующий этаж')
    elif position.get('Corpus') in ['Академика Волгина 2/1', 'Академика Волгина 2/2']:
        if text in ['1', '2', '3', '4', '5',
                    '6', '7', '8', '9', '10',
                    '11', '12', '13', '14', '15', '16']:
            await message.answer(text='Укажите блок\n\n'
                                      'Если нарушение происходит не в блоке (в коридоре, на кухне, на лестничной'
                                      " площадке), или вы не знаете точно где, выберите 'Этаж' и "
                                      'в комментарии уточните информацию',
                                 reply_markup=create_block(text))
            await Position.block.set()
            async with state.proxy() as data:
                data['Floor'] = text
        else:
            await message.answer(text='Укажите существующий этаж')


@dp.message_handler(state=Position.block)
async def enter_block(message: types.Message, state: FSMContext):
    text = message.text
    position = await state.get_data()
    floor = position.get('Floor')
    corpus = position.get('Corpus')
    if text == 'Назад':
        if corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5']:
            await message.answer(text='Укажите этаж', reply_markup=floor_15_markup)
        else:
            await message.answer(text='Укажите этаж', reply_markup=floor_16_markup)
        await Position.previous()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif text == 'Этаж':
        await message.answer(text='Укажите причину вашего обращения\n\n'
                                  "Если вы не нашли нужную кнопку, выберите 'Другое' и опишите ситуацию",
                             reply_markup=motive_markup)
        await Position.motive.set()
        async with state.proxy() as data:
            data['Block'] = text
    elif text in [floor + '01', floor + '02', floor + '03', floor + '04', floor + '05',
                    floor + '06', floor + '07', floor + '08', floor + '09', floor + '10',
                    floor + '11', floor + '12', floor + '13', floor + '14', floor + '15',
                    floor + '16', floor + '17', floor + '18']:
        await message.answer(text='Укажите комнату\n\n'
                                  'Если вы точно не знаете комнату, выберите только номер блока',
                             reply_markup=create_room(text))
        await Position.room.set()
        async with state.proxy() as data:
            data['Block'] = text
    else:
        await message.answer(text='Укажите существующий блок')


@dp.message_handler(state=Position.room)
async def enter_room(message: types.Message, state: FSMContext):
    text = message.text
    position = await state.get_data()
    floor = position.get('Floor')
    block = position.get('Block')
    if text == 'Назад':
        await message.answer(text='Укажите блок\n\n'
                                  'Если нарушение происходит не в блоке (в коридоре, на кухне, на лестничной'
                                  " площадке), или вы не знаете точно где, выберите 'Этаж' и "
                                  'в комментарии уточните информацию',
                             reply_markup=create_block(floor))
        await Position.previous()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif text in [block + '/3', block + '/2', block]:
        await message.answer(text='Укажите причину вашего обращения\n\n'
                                  "Если вы не нашли нужную кнопку, выберите 'Другое' и опишите ситуацию",
                             reply_markup=motive_markup)
        await Position.motive.set()
        async with state.proxy() as data:
            data['Room'] = text
    else:
        await message.answer(text='Укажите существующую комнату')


@dp.message_handler(state=Position.motive)
async def enter_motive(message: types.Message, state: FSMContext):
    text = message.text
    position = await state.get_data()
    floor = position.get('Floor')
    block = position.get('Block')
    if text == 'Назад':
        if block == 'Этаж':
            await message.answer(text='Укажите блок\n\n'
                                      'Если нарушение происходит не в блоке (в коридоре, на кухне, на лестничной'
                                      " площадке), или вы не знаете точно где, выберите 'Этаж' и "
                                      'в комментарии уточните информацию',
                                 reply_markup=create_block(floor))
            await Position.block.set()
        else:
            await message.answer(text='Укажите комнату\n\n'
                                      'Если вы точно не знаете комнату, выберите только номер блока',
                                 reply_markup=create_room(block))
            await Position.previous()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif text in ['Запах табака, курительных смесей', 'Шум', 'Другое']:
        await message.answer(text='Опишите ситуцию (не более 200 символов)', reply_markup=comment_markup)
        await Position.comment.set()
        async with state.proxy() as data:
            data['Motive'] = text
    else:
        await message.answer(text='Укажите причину из данного списка:\n\n'
                                  '▪️Запах табака, курительных смесей\n'
                                  '▪️Шум\n'
                                  '▪️Другое')


@dp.message_handler(state=Position.comment)
async def enter_comment(message: types.Message, state: FSMContext):
    text = message.text
    position = await state.get_data()
    corpus = position.get('Corpus')
    floor = position.get('Floor')
    block = position.get('Block')
    room = position.get('Room')
    motive = position.get('Motive')
    if text == 'Назад':
        await message.answer(text='Укажите причину вашего обращения\n\n'
                                  "Если вы не нашли нужную кнопку, выберите 'Другое' и опишите ситуацию",
                             reply_markup=motive_markup)
        await Position.previous()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    elif text == 'Пропустить':
        if block == 'Этаж':
            confirm_text = f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                           f'<i>Этаж:</i> <b>{floor}</b>\n' \
                           f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                           f'<i>Комментарий:</i> _'
        else:
            confirm_text = f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                           f'<i>Блок:</i> <b>{room}</b>\n' \
                           f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                           f'<i>Комментарий:</i> _'
        await message.answer(text='Подтвердите обращение:\n\n' + confirm_text, reply_markup=confirm_markup)
        await Position.confirmation.set()
        async with state.proxy() as data:
            data['Comment'] = '_'
    else:
        if block == 'Этаж':
            confirm_text = f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                           f'<i>Этаж:</i> <b>{floor}</b>\n' \
                           f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                           f'<i>Комментарий:</i> <b>{text[:min(len(text), 200)]}</b>'
        else:
            confirm_text = f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                           f'<i>Блок:</i> <b>{room}</b>\n' \
                           f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                           f'<i>Комментарий:</i> <b>{text[:min(len(text), 200)]}</b>'
        await message.answer(text='Подтвердите обращение:\n\n' + confirm_text, reply_markup=confirm_markup)
        await Position.confirmation.set()
        async with state.proxy() as data:
            data['Comment'] = text[:min(len(text), 200)]


@dp.message_handler(state=Position.confirmation)
async def enter_confirm(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    nickname = message.from_user.username
    position = await state.get_data()
    corpus = position.get('Corpus')
    floor = position.get('Floor')
    block = position.get('Block')
    room = position.get('Room')
    motive = position.get('Motive')
    comment = position.get('Comment')

    if text == 'Назад':
        await message.answer(text='Опишите ситуацию (не более 200 символов)', reply_markup=comment_markup)
        await Position.previous()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие ⬇️', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Отправить жалобу':
        dt = datetime.now() + timedelta(hours=time_zone)
        if block == 'Этаж':
            answer_text = f'<i>Пользователь:</i> <b>{user_name} (@{nickname}, <code>{user_id}</code>)</b>\n' \
                          f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                          f'<i>Этаж:</i> <b>{floor}</b>\n' \
                          f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                          f'<i>Комментарий:</i> <b>{comment[:min(len(comment), 200)]}</b>'
            await commands_complaint.add_complaint(user_id=user_id, user_name=user_name, date_time=dt,
                                                   corpus=corpus, floor=floor,
                                                   block=block, room=None, motive=motive,
                                                   comment=comment[:min(len(comment), 200)],
                                                   status='Не обработано', nickname=nickname)
        else:
            answer_text = f'<i>Пользователь:</i> <b>{user_name} (@{nickname}, <code>{user_id}</code>)</b>\n' \
                          f'<i>Корпус:</i> <b>{corpus}</b>\n' \
                          f'<i>Блок:</i> <b>{room}</b>\n' \
                          f'<i>Нарушение:</i> <b>{motive}</b>\n' \
                          f'<i>Комментарий:</i> <b>{comment[:min(len(comment), 200)]}</b>'
            await commands_complaint.add_complaint(user_id=user_id, user_name=user_name, date_time=dt,
                                                   corpus=corpus, floor=floor,
                                                   block=block, room=room, motive=motive,
                                                   comment=comment[:min(len(comment), 200)],
                                                   status='Не обработано', nickname=nickname)

        await message.answer(text='Жалоба отправлена. Спасибо!', reply_markup=start_markup)
        alerts = await commands_alert.select_all_alerts()
        for admin in admins:
            for alert in alerts:
                if admin == alert.user_id and corpus == alert.corpus and alert.status:
                    try:
                        await bot.send_message(chat_id=admin, text=answer_text)
                    except:
                        pass
                    finally:
                        break

        await state.finish()
        await Starting.choose.set()

    else:
        await message.answer(text='Выберите одно из трёх действий:\n\n'
                                  '▪️Отправить жалобу\n'
                                  '▪️Назад\n'   
                                  '▪️Отмена', reply_markup=confirm_markup)