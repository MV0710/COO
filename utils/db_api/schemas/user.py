from utils.db_api.db_gino import TimeBaseModel
from sqlalchemy import Column, String, Integer, Text, sql, DateTime, BigInteger


class LOL(TimeBaseModel):
    __tablename__ = 'Users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(255))
    created = Column(DateTime, nullable=False)
    blocking = Column(Integer, nullable=False)
    last_edit = Column(DateTime, nullable=False)
    nickname = Column(String(255))

    query: sql.Select