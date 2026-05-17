from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from .base import Base

class DangKy(Base):
    __tablename__ = 'dang_ky'
    # Sử dụng Integer tự tăng để tránh xung đột mã khi đăng ký đồng thời
    ma_dk = Column(Integer, primary_key=True, autoincrement=True)
    # ma_sv không để ForeignKey để hỗ trợ SV site này đăng ký lớp site kia
    ma_sv = Column(String(20), nullable=False) 
    ma_lop_hp = Column(String(20), ForeignKey('lop_hoc_phan.ma_lop_hp'))
    thoi_gian_dang_ky = Column(DateTime, server_default=func.now())
    trang_thai = Column(String(50), default='THANH_CONG')
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
