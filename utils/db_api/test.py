import asyncio

from data import config
from utils.db_api import quick_commands, commands_alert
from utils.db_api.db_gino import db


async def test():
    await db.set_bind(config.POSTGRES_URL)
    print(1)
    await db.gino.drop_all()
    await db.gino.create_all()
    await quick_commands.add_user(1, "one", "email.com")
    #await quick_commands.update_user_email(1,"Fuck.com")
    #await commands_alert.add_alert(586619481, "a", True)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
