from aiogram import types
from keyboards.default.start import start_markup

from states import Starting

from loader import dp, bot
from utils.misc import rate_limit


@rate_limit(limit=10, key='Документация')
@dp.message_handler(text='Документация', state=Starting.choose)
async def f_docs(message: types.Message):
    await bot.send_document(chat_id=message.from_user.id,
                            document='C:/Users/Maks/Downloads/Telegram Desktop/Правила_внутреннего_распорядка_обучающихся.pdf')
    await bot.send_document(chat_id=message.from_user.id,
                            document='BQACAgIAAxkBAAMRY_CU4t-r7k3_TRPNOOOyOQ2IGy8AAiEhAAIG_YlL-no1jGPkXLEuBA')
    await bot.send_document(chat_id=message.from_user.id,
                            document='BQACAgIAAxkBAAMTY_CU9G86DhsoovVf5KxH9B1YH-4AAiIhAAIG_YlLScPvy80AAe7OLgQ',
                            reply_markup=start_markup)