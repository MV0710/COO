from sqlalchemy import Column, Integer, sql, DateTime, String, BigInteger

from utils.db_api.postgresql import BaseModel

class User(BaseModel):
    __tablename__ = 'Users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(255))
    created = Column(DateTime, nullable=False)
    blocking = Column(Integer, nullable=False)
    last_edit = Column(DateTime, nullable=False)
    nickname = Column(String(255))

    query: sql.Select