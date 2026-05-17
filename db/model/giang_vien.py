from sqlalchemy import Column, String, ForeignKey, Boolean
from .base import Base

class GiangVien(Base):
    __tablename__ = 'giang_vien'
    ma_gv = Column(String(20), primary_key=True)
    ho_ten = Column(String(100), nullable=False)
    hoc_vi = Column(String(50))
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
    da_xoa = Column(Boolean, default=False)
