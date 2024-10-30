from utils.db_api.tables.alert import Alert

from loader import bot


async def add_alert(user_id: int, corpus: str, status: bool):
    try:
        alert = Alert(user_id=user_id, corpus=corpus, status=status)
        await alert.create()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: add_alert\n"
                                                       f"PARAMETERS: user_id={user_id}, corpus={corpus}, "
                                                       f"status={status}\n"
                                                       f"EXCEPTION: {ex}")


async def select_all_alerts():
    try:
        alerts = await Alert.query.gino.all()
        return alerts

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_all_alerts\n"
                                                       f"EXCEPTION: {ex}")
        return []


async def select_alerts(user_id):
    try:
        alerts = await Alert.query.where(Alert.user_id == user_id).gino.all()
        return alerts

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_alerts\n"
                                                       f"PARAMETERS: user_id={user_id}\n"
                                                       f"EXCEPTION: {ex}")
        return []


async def update_alert(user_id, corpus, status):
    try:
        alert = await Alert.query.where((Alert.user_id == user_id) & (Alert.corpus == corpus)).gino.first()
        await alert.update(status=status).apply()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: update_alert\n"
                                                       f"PARAMETERS: user_id={user_id}, corpus={corpus}, "
                                                       f"status={status}\n"
                                                       f"EXCEPTION: {ex}")


