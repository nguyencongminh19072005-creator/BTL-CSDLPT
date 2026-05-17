from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from .base import Base

class LopHocPhan(Base):
    __tablename__ = 'lop_hoc_phan'
    ma_lop_hp = Column(String(20), primary_key=True)
    ma_hp = Column(String(20), ForeignKey('hoc_phan.ma_hp'))
    # ma_gv để String, không đặt ForeignKey để hỗ trợ giảng viên dạy liên site
    ma_gv = Column(String(20)) 
    ma_phong = Column(String(20), ForeignKey('phong_hoc.ma_phong'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
    hoc_ky = Column(Integer)
    nam_hoc = Column(String(20))
    si_so_toi_da = Column(Integer)
    so_luong_da_dang_ky = Column(Integer, default=0)
    
    # TRỌNG TÂM: Cột version để dùng Optimistic Locking xử lý đồng thời
    version = Column(Integer, default=0, nullable=False)

    __mapper_args__ = {
        "version_id_col": version
    }

    __table_args__ = (
        CheckConstraint('so_luong_da_dang_ky <= si_so_toi_da', name='check_siso_limit'),
    )
