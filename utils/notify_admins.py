import logging

from aiogram import Dispatcher


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(586619481, "Бот Запущен и готов к работе")

    except Exception as err:
        logging.exception(err)
