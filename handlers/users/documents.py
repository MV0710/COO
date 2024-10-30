from aiogram import types
from keyboards.default.start import start_markup

from states import Starting

from loader import dp, bot
from utils.misc import rate_limit


@rate_limit(limit=10, key='Документация')
@dp.message_handler(text='Документация', state=Starting.choose)
async def f_docs(message: types.Message):
    f1 = open('Правила_внутреннего_распорядка_обучающихся.pdf', 'rb')
    f2 = open('Устав Университета.pdf', 'rb')
    f3 = open('Правила_проживания_в_студенческом_городке.pdf', 'rb')
    await bot.send_document(chat_id=message.from_user.id, document=f1)
    await bot.send_document(chat_id=message.from_user.id, document=f2) 
    await bot.send_document(chat_id=message.from_user.id, document=f3, reply_markup=start_markup)
