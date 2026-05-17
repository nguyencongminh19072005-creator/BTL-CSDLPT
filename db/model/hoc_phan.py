from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class HocPhan(Base):
    __tablename__ = 'hoc_phan'
    ma_hp = Column(String(20), primary_key=True)
    ten_hp = Column(String(100), nullable=False)
    so_tin_chi = Column(Integer, nullable=False)
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))
