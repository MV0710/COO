from sqlalchemy import Column, String, Integer, Text, sql, DateTime, BigInteger

from utils.db_api.postgresql import BaseModel


class Complaint(BaseModel):
    __tablename__ = 'Complaints'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(255))
    date_time = Column(DateTime, nullable=False)
    corpus = Column(String(255), nullable=False)
    floor = Column(String(255), nullable=False)
    block = Column(String(255))
    room = Column(String(255))
    motive = Column(String(255), nullable=False)
    comment = Column(Text)
    status = Column(String(255), nullable=False)
    nickname = Column(String(255))

    query: sql.Select