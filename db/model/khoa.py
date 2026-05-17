from sqlalchemy import Column, String
from .base import Base

class Khoa(Base):
    __tablename__ = 'khoa'
    ma_khoa = Column(String(20), primary_key=True)
    ten_khoa = Column(String(100), nullable=False)
