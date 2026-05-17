import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))

from config_db import SessionLocals as SessionLocal
from model import SinhVien, DangKy, LopHocPhan

def check_cross_site_registration():
    print("DANG TIM KIEM DAU VET CUA SINH VIEN 'SV_HD_001' TREN TOAN HE THONG...\n")
    
    # Duyệt qua cả 3 máy chủ
    for site in ["HD", "CG", "NT"]:
        session = SessionLocal[site]()
        
        # Tìm xem SV_HD_001 có đăng ký môn nào ở máy chủ này không
        ket_qua = session.query(DangKy, LopHocPhan)\
            .join(LopHocPhan, DangKy.ma_lop_hp == LopHocPhan.ma_lop_hp)\
            .filter(DangKy.ma_sv == 'SV_HD_001').all()
            
        if ket_qua:
            print(f"TAI SERVER {site} (Co so {site}):")
            for dk, lhp in ket_qua:
                print(f"   - Đang học lớp: {lhp.ma_lop_hp}")
                print(f"   - Mã môn học: {lhp.ma_hp}")
                print(f"   - Do giảng viên: {lhp.ma_gv} giảng dạy")
            print("-" * 40)
            
        session.close()

if __name__ == "__main__":
    check_cross_site_registration()
