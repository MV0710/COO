from aiogram import types

from loader import dp


@dp.message_handler()
async def f_rules(message: types.Message):
    await message.answer(text="Бот был перезапущен.\nВведите команду '/start' для начала работы.")
    #await message.answer(text='Ведутся работы по обновлению. Пожалуйста, подождите.\n'
                              #'Мы закончим в течении 5-10 минут')