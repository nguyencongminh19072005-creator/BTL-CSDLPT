import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.config_db import SessionLocals as SessionLocal
from db.model import LopHocPhan, HocPhan

def xem_danh_sach_lop_toan_truong():
    print("\n🔍 Đang quét dữ liệu từ các phân mảnh (Hà Đông, Cầu Giấy, Ngọc Trục)...")
    print(f"{'MÃ LỚP':<15} | {'TÊN MÔN HỌC':<20} | {'SĨ SỐ':<10} | {'CƠ SỞ':<10}")
    print("-" * 65)

    sites = ['HD', 'CG', 'NT']
    tong_so_lop = 0

    for site in sites:
        session = SessionLocal[site]()
        try:
            # Gom dữ liệu từ Lớp học phần và Môn học
            danh_sach = session.query(LopHocPhan, HocPhan).join(
                HocPhan, LopHocPhan.ma_hp == HocPhan.ma_hp
            ).all()
            
            for lop, hp in danh_sach:
                si_so_str = f"{lop.so_luong_da_dang_ky}/{lop.si_so_toi_da}"
                print(f"{lop.ma_lop_hp:<15} | {hp.ten_hp:<20} | {si_so_str:<10} | {site:<10}")
                tong_so_lop += 1
        except Exception as e:
            print(f"❌ Lỗi truy xuất tại cơ sở {site}: {e}")
        finally:
            session.close()

    print("-" * 65)
    print(f"✅ Tổng cộng: {tong_so_lop} lớp học phần trên toàn hệ thống.\n")
