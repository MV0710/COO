from utils.db_api.db_gino import TimeBaseModel
from sqlalchemy import Column, String, Integer, Text, sql, DateTime, BigInteger, Boolean


class LOL(TimeBaseModel):
    __tablename__ = 'Alerts'
    user_id = Column(BigInteger, primary_key=True)
    corpus = Column(String(255), primary_key=True)
    status = Column(Boolean, nullable=False)

    query: sql.Select