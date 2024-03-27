from datetime import datetime

from loader import bot
from utils.db_api.tables.message import Message


async def add_mg(admin_id: int, complaint_id: int, date_time: datetime, mg: str):
    try:
        message = Message(admin_id=admin_id, complaint_id=complaint_id, date_time=date_time, mg=mg)
        await message.create()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: add_mg\n"
                                                       f"PARAMETERS: admin_id={admin_id}, complaint_id={complaint_id}, "
                                                       f"date_time={date_time}, mg={mg}"
                                                       f"EXCEPTION: {ex}")


async def select_mg(complaint_id: int):
    try:
        mg = await Message.query.where(Message.complaint_id == complaint_id).gino.all()
        mg.sort(key=lambda x: x.id)
        return mg

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_mg\n"
                                                       f"PARAMETERS: complaint_id={complaint_id}\n"
                                                       f"EXCEPTION: {ex}")
        return []
