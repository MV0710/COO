from sqlalchemy import Column, sql, Integer, BigInteger, Text, DateTime, String

from utils.db_api.postgresql import BaseModel


class Message(BaseModel):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger)
    complaint_id = Column(Integer)
    date_time = Column(DateTime)
    mg = Column(Text)

    query: sql.Select