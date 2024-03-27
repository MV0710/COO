from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from utils.db_api import commands_alert

from data.config import admins
from keyboards.default import start_markup, confirm_status, corpus_edit_status, edit_status
from loader import dp
from states import Info, Starting


@dp.message_handler(Command('send'), user_id=admins, state=Starting.choose)
async def make_alert(message: types.Message, state: FSMContext):
    admin_id = message.from_user.id
    await state.update_data(
        {
            'edit_corpus': set()
        }
    )

    alerts = await commands_alert.select_alerts(user_id=admin_id)
    answer_text = 'Текущий статус:\n\n'
    for corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
        for alert in alerts:
            if corpus == alert.corpus and alert.status:
                answer_text += f'{corpus}: Да\n'
                break
            elif corpus == alert.corpus and not alert.status:
                answer_text += f'{corpus}: Нет\n'
                break

    await message.answer(text=answer_text, reply_markup=confirm_status)
    await Info.confirm_status.set()


@dp.message_handler(user_id=admins, state=Info.confirm_status)
async def confirm_alert(message: types.Message, state: FSMContext):
    text = message.text
    if text == 'Изменить':
        await message.answer(text='Статус каких корпусов вы хотите поменять?', reply_markup=corpus_edit_status)
        await Info.corpus_edit_status.set()
    elif text == 'Назад':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    else:
        await message.answer(text='Выберите один из предложенных вариантов')


@dp.message_handler(user_id=admins, state=Info.corpus_edit_status)
async def corpus_alert(message: types.Message, state: FSMContext):
    text = message.text
    if text in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
        data = await state.get_data()
        edit_corpus = data.get('edit_corpus')
        edit_corpus.add(text)
        await state.update_data(
            {
                'edit_corpus': edit_corpus
            }
        )
        new_text = ''
        for corpus in edit_corpus:
            new_text += corpus + '\n'
        await message.answer(text=new_text, reply_markup=corpus_edit_status)
    elif text == 'Далее':
        await message.answer(text='Выберите изменение', reply_markup=edit_status)
        await Info.edit_status.set()
    elif text == 'Отмена':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()
    else:
        await message.answer(text='Выберите один из предложенных вариантов')


@dp.message_handler(user_id=admins, state=Info.edit_status)
async def edit_alert(message: types.Message, state: FSMContext):
    text = message.text
    admin_id = message.from_user.id
    edit_corpus = (await state.get_data()).get('edit_corpus')
    answer_text = ''
    if text == 'Отправлять':
        for corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
            if corpus in edit_corpus:
                await commands_alert.update_alert(user_id=admin_id, corpus=corpus, status=True)

        alerts = await commands_alert.select_alerts(user_id=admin_id)

        for corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
            for alert in alerts:
                if corpus == alert.corpus and alert.status:
                    answer_text += f'{corpus}: Да\n'
                    break
                elif corpus == alert.corpus and not alert.status:
                    answer_text += f'{corpus}: Нет\n'
                    break

        await message.answer(text='Обновленный статус:\n\n'+answer_text, reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Не отправлять':
        for corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
            if corpus in edit_corpus:
                await commands_alert.update_alert(user_id=admin_id, corpus=corpus, status=False)

        alerts = await commands_alert.select_alerts(user_id=admin_id)

        for corpus in ['Бутлерова 1', 'Бутлерова 3', 'Бутлерова 5', 'Академика Волгина 2/1', 'Академика Волгина 2/2']:
            for alert in alerts:
                if corpus == alert.corpus and alert.status:
                    answer_text += f'{corpus}: Да\n'
                    break
                elif corpus == alert.corpus and not alert.status:
                    answer_text += f'{corpus}: Нет\n'
                    break

        await message.answer(text='Обновленный статус:\n\n' + answer_text, reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    elif text == 'Отмена':
        await message.answer(text='Выберите действие', reply_markup=start_markup)
        await state.finish()
        await Starting.choose.set()

    else:
        await message.answer(text='Выберите один из предложенных вариантов')