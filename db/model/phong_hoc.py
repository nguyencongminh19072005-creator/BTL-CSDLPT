from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class PhongHoc(Base):
    __tablename__ = 'phong_hoc'
    ma_phong = Column(String(20), primary_key=True)
    ten_phong = Column(String(100), nullable=False)
    suc_chua = Column(Integer)
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
