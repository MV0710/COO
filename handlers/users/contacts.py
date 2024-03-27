from aiogram import types
from keyboards.default.start import start_markup

from states import Starting

from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=10, key='Контакты')
@dp.message_handler(text='Контакты', state=Starting.choose)
async def f_contacts(message: types.Message):
    await message.answer(text='<b>Командир СОО:</b> <a href="https://vk.com/vd_023">Даценко Вячеслав Игоревич</a>\n')
    await message.answer(text='<b>Зам. командира СОО:</b> <a href="https://vk.com/tokareva_01">Токарева Екатерина Андреевна</a>\n')
    await message.answer(text='<b>Зам. командира СОО:</b> <a href="https://vk.com/damir56426">Сафаралиев Дамир Надырович</a>',
                         reply_markup=start_markup)