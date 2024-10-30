from sqlalchemy import Column, String, Boolean, sql, BigInteger, create_engine

from utils.db_api.postgresql import BaseModel

class Alert(BaseModel):
    __tablename__ = 'Alerts'
    user_id = Column(BigInteger, primary_key=True)
    corpus = Column(String(255), primary_key=True)
    status = Column(Boolean, nullable=False)

    query: sql.Select