from loader import bot
from utils.db_api.tables.complaint import Complaint

from datetime import datetime


async def add_complaint(user_id: int, user_name: str, date_time: datetime, corpus: str, floor: str, block: str = None,
        room: str = None, motive: str = 'Другое', comment: str = None, status: str = 'Не обработано', nickname: str = ' '):
    try:
        complaint = Complaint(user_id=user_id, user_name=user_name, date_time=date_time, corpus=corpus, floor=floor,
                                     block=block, room=room, motive=motive, comment=comment, status=status, nickname=nickname)
        await complaint.create()
    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: add_complaint\n"
                                                       f"PARAMETERS: user_id={user_id}, user_name={user_name}"
                                                       f"date_time={date_time}"
                                                       f", corpus={corpus}, floor={floor}, block={block}, "
                                                       f"room={room}, motive={motive}, comment={comment}, "
                                                       f"status={status}, nickname={nickname}\n"
                                                       f"EXCEPTION: {ex}")


async def select_all_complaints():
    try:
        complaints = await Complaint.query.gino.all()
        complaints.sort(key=lambda x: x.id)
        return complaints

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_all_complaints\n"
                                                       f"EXCEPTION: {ex}")
        return []


async def select_complaints(corpus, status):
    try:
        complaints = await Complaint.query.where((Complaint.corpus == corpus) & (Complaint.status == status)).gino.all()
        complaints.sort(key=lambda x: x.id, reverse=True)
        return complaints

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_complaints\n"
                                                       f"PARAMETERS: corpus={corpus}, status={status}\n"
                                                       f"EXCEPTION: {ex}")
        return []


async def update_complaints(corpus, block, status):
    try:
        complaints = await Complaint.query.where((Complaint.corpus == corpus) & (Complaint.block == block)).gino.all()
        for complaint in complaints:
            await complaint.update(status=status).apply()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: update_complaints\n"
                                                       f"PARAMETERS: corpus={corpus}, block={block}, status={status}\n"
                                                       f"EXCEPTION: {ex}")


async def update_complaints_floor(corpus, block, floor, status):
    try:
        complaints = await Complaint.query.where((Complaint.corpus == corpus) & (Complaint.block == block) &
                                                 (Complaint.floor == floor)).gino.all()
        for complaint in complaints:
            await complaint.update(status=status).apply()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: update_complaints_floor\n"
                                                       f"PARAMETERS: corpus={corpus}, block={block}, floor={floor}"
                                                       f"status={status}\n"
                                                       f"EXCEPTION: {ex}")


async def select_complaints_user(user_id):
    try:
        complaints = await Complaint.query.where(Complaint.user_id == user_id).gino.all()
        complaints.sort(key=lambda x: x.id, reverse=True)
        return complaints

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_complaints_user\n"
                                                       f"PARAMETERS: user_id={user_id}\n"
                                                       f"EXCEPTION: {ex}")
        return []
