from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, DateTime, CheckConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

# =================================================================
# 1. NHÓM BẢNG DANH MỤC (NHÂN BẢN - REPLICATED TRÊN 3 SITE)
# =================================================================

class CoSo(Base):
    __tablename__ = 'co_so'
    ma_co_so = Column(String(20), primary_key=True)
    ten_co_so = Column(String(100), nullable=False)
    dia_chi = Column(String(255))

class Khoa(Base):
    __tablename__ = 'khoa'
    ma_khoa = Column(String(20), primary_key=True)
    ten_khoa = Column(String(100), nullable=False)

class HocPhan(Base):
    __tablename__ = 'hoc_phan'
    ma_hp = Column(String(20), primary_key=True)
    ten_hp = Column(String(100), nullable=False)
    so_tin_chi = Column(Integer, nullable=False)
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))

# =================================================================
# 2. NHÓM BẢNG THỰC THỂ (PHÂN MẢNH THEO SITE)
# =================================================================

class SinhVien(Base):
    __tablename__ = 'sinh_vien'
    ma_sv = Column(String(20), primary_key=True)
    ho_ten = Column(String(100), nullable=False)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(10))
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
    da_xoa = Column(Boolean, default=False)

class GiangVien(Base):
    __tablename__ = 'giang_vien'
    ma_gv = Column(String(20), primary_key=True)
    ho_ten = Column(String(100), nullable=False)
    hoc_vi = Column(String(50))
    ma_khoa = Column(String(20), ForeignKey('khoa.ma_khoa'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))
    da_xoa = Column(Boolean, default=False)

class PhongHoc(Base):
    __tablename__ = 'phong_hoc'
    ma_phong = Column(String(20), primary_key=True)
    ten_phong = Column(String(100), nullable=False)
    suc_chua = Column(Integer)
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))

# =================================================================
# 3. NHÓM BẢNG NGHIỆP VỤ (GIAO DỊCH VÀ ĐĂNG KÝ)
# =================================================================

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

    __table_args__ = (
        CheckConstraint('so_luong_da_dang_ky <= si_so_toi_da', name='check_siso_limit'),
    )

class LichHoc(Base):
    __tablename__ = 'lich_hoc'
    ma_lich = Column(String(20), primary_key=True)
    ma_lop_hp = Column(String(20), ForeignKey('lop_hoc_phan.ma_lop_hp'))
    thu = Column(Integer)
    tiet_bat_dau = Column(Integer)
    tiet_ket_thuc = Column(Integer)
    ma_phong = Column(String(20), ForeignKey('phong_hoc.ma_phong'))
    ma_co_so = Column(String(20), ForeignKey('co_so.ma_co_so'))

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

# =================================================================
# 4. CẤU HÌNH KẾT NỐI VÀ KHỞI TẠO (DOCKER)
# =================================================================

# URL kết nối tới 3 máy (Khớp với các Port bạn đã map trong Docker)
DATABASE_URLS = {
    "HD": "postgresql://postgres:123456@localhost:5435/qldt_hadong",
    "CG": "postgresql://postgres:123456@localhost:5433/qldt_caugiay",
    "TN": "postgresql://postgres:123456@localhost:5434/qldt_trucngoc"
}

engines = {site: create_engine(url) for site, url in DATABASE_URLS.items()}
SessionLocal = {site: sessionmaker(bind=eng, autocommit=False, autoflush=False) for site, eng in engines.items()}

def init_db():
    """Hàm chạy một lần để tạo toàn bộ cấu trúc bảng trên 3 Server"""
    for site, engine in engines.items():
        print(f"🛠️ Đang khởi tạo bảng tại Site: {site}...")
        try:
            Base.metadata.create_all(engine)
            print(f"✅ Hoàn tất Site {site}")
        except Exception as e:
            print(f"❌ Lỗi tại {site}: {e}")

if __name__ == "__main__":
    init_db()