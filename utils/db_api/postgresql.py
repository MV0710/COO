from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa

from data import config

db = Gino()
class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


async def on_startup(dispatcher: Dispatcher):
    print('Connected PostgreSQL')
    await db.set_bind(config.POSTGRES_URL)

