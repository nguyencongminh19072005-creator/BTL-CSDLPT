from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
try:
    from .model import Base, CoSo, Khoa, HocPhan, SinhVien, GiangVien, PhongHoc, LopHocPhan, LichHoc, DangKy
except (ImportError, ValueError):
    from model import Base, CoSo, Khoa, HocPhan, SinhVien, GiangVien, PhongHoc, LopHocPhan, LichHoc, DangKy

# =================================================================
# 4. CẤU HÌNH KẾT NỐI VÀ KHỞI TẠO (DOCKER)
# =================================================================

# URL kết nối tới 3 máy (Khớp với các Port bạn đã map trong Docker)
DATABASE_URLS = {
    "HD": "postgresql://postgres:123456@localhost:5435/qldt_hadong",
    "CG": "postgresql://postgres:123456@localhost:5433/qldt_caugiay",
    "NT": "postgresql://postgres:123456@localhost:5434/qldt_ngoctruc"
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