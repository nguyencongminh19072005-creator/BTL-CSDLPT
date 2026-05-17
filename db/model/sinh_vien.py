from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from .base import Base

class SinhVien(Base):
    __tablename__ = 'sinh_vien'
    ma_sv = Column(String(20), primary_key=True)
    ho_ten = Column(String(100), nullable=False)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(10))
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
    da_xoa = Column(Boolean, default=False)
