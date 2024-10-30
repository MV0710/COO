from utils.db_api.db_gino import TimeBaseModel
from sqlalchemy import Column, String, Integer, Text, sql, DateTime, BigInteger, Boolean


class LOL(TimeBaseModel):
    __tablename__ = 'LOL'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), primary_key=True)
    email = Column(String(255), primary_key=True)

    query: sql.Select