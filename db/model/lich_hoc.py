from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class LichHoc(Base):
    __tablename__ = 'lich_hoc'
    ma_lich = Column(String(20), primary_key=True)
    ma_lop_hp = Column(String(20), ForeignKey('lop_hoc_phan.ma_lop_hp'))
    thu = Column(Integer)
    tiet_bat_dau = Column(Integer)
    tiet_ket_thuc = Column(Integer)
    ma_phong = Column(String(20), ForeignKey('phong_hoc.ma_phong'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
