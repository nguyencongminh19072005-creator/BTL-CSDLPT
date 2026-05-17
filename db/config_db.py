import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

# Cấu hình kết nối tới 3 cơ sở bằng SQLAlchemy URL
DB_URLS = {
    "HD": "postgresql+psycopg2://postgres:123456@localhost:5435/qldt_hadong",
    "CG": "postgresql+psycopg2://postgres:123456@localhost:5433/qldt_caugiay",
    "NT": "postgresql+psycopg2://postgres:123456@localhost:5434/qldt_ngoctruc",
}

engines = {}
SessionLocals = {}

for site, url in DB_URLS.items():
    engine = create_engine(url, echo=False)
    engines[site] = engine
    SessionLocals[site] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db(site_code):
    """Mở kết nối tới một site cụ thể và yield session (dùng cho FastAPI Depends)."""
    if site_code not in SessionLocals:
        raise ValueError(f"❌ Mã cơ sở '{site_code}' không tồn tại trong cấu hình.")
    db = SessionLocals[site_code]()
    try:
        yield db
    finally:
        db.close()

def init_all_dbs():
    """Tạo toàn bộ các bảng trong models.py trên cả 3 Server."""
    print("Dang khoi tao cac bang CSDL tren toan he thong phan tan...")
    for site, engine in engines.items():
        try:
            Base.metadata.create_all(bind=engine)
            print(f"Da tao bang thanh cong tai Node: {site}")
        except Exception as e:
            print(f"Loi khi tao bang tai Node {site}: {e}")

if __name__ == "__main__":
    init_all_dbs()