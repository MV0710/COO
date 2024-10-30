from asyncpg import UniqueViolationError

from utils.db_api.schemas.LOL import LOL

async def add_user(id: int, name: str, email: str =None):
    try:
        lol = LOL(id=id, name=name, email=email)

        await lol.create()
    except UniqueViolationError:
        pass

async def update_user_email(id, email):
    user = await LOL.get(id)
    await user.update(email=email).apply()