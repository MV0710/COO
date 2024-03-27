from sqlalchemy import Column, sql, BigInteger, Integer, DateTime

from utils.db_api.postgresql import BaseModel


class Update(BaseModel):
    __tablename__ = 'Updates'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    old_status = Column(Integer, nullable=False)
    new_status = Column(Integer, nullable=False)
    admin_id = Column(BigInteger, nullable=False)
    date_time = Column(DateTime, nullable=False)

    query: sql.Select