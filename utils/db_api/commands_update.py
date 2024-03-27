from loader import bot

from datetime import datetime

from utils.db_api.tables.update_user import Update


async def add_update(user_id: int, old_status: int, new_status: int, admin_id: int, date_time: datetime):
    try:
        update = Update(user_id=user_id, old_status=old_status, new_status=new_status,
                           admin_id=admin_id, date_time=date_time)
        await update.create()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: add_update\n"
                                                       f"PARAMETERS: id={id}, old_status={old_status}, "
                                                       f"new_status={new_status}, admin_id={admin_id}, "
                                                       f"date_time={date_time}\n"
                                                       f"EXCEPTION: {ex}")