from sqlalchemy import Column, String
from .base import Base

class CoSo(Base):
    __tablename__ = 'co_so'
    ma_co_so = Column(String(20), primary_key=True)
    ten_co_so = Column(String(100), nullable=False)
    dia_chi = Column(String(255))
