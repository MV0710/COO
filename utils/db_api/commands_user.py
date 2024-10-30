from utils.db_api.tables.user import User

from datetime import datetime

from loader import bot


async def add_user(user_id: int, user_name: str, created: datetime, blocking: int, last_edit: datetime, nickname: str):
    try:
        user = User(user_id=user_id, user_name=user_name, created=created, blocking=blocking, last_edit=last_edit, nickname=nickname)
        await user.create()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: add_user\n"
                                                       f"PARAMETERS: user_id={user_id}, user_name={user_name}"
                                                       f"nickname={nickname}, created={created}, "
                                                       f"blocking={blocking}, last_edit={last_edit}\n"
                                                       f"EXCEPTION: {ex}")


async def update_user(user_id, blocking, last_edit):
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        await user.update(blocking=blocking, last_edit=last_edit).apply()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: update_user\n"
                                                       f"PARAMETERS: user_id={user_id}, blocking={blocking},"
                                                       f" last_edit={last_edit}\n"
                                                       f"EXCEPTION: {ex}")


async def update_user_nickname(user_id, nickname):
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        await user.update(nickname=nickname).apply()

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: update_user_nickname\n"
                                                       f"PARAMETERS: user_id={user_id}, "
                                                       f" nickname={nickname}\n"
                                                       f"EXCEPTION: {ex}")


async def select_user(user_id):
    try:
        user = await User.query.where(User.user_id == user_id).gino.all()
        return user

    except Exception as ex:
        await bot.send_message(chat_id=586619481, text="ERROR\n"
                                                       "FUNC: select_user\n"
                                                       f"PARAMETERS: user_id={user_id}\n"
                                                       f"EXCEPTION: {ex}")
        return []