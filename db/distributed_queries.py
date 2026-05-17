import sys
import os
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.query import get_lop_toan_truong_site

def xem_danh_sach_lop_toan_truong():
    print("\n🔍 Đang quét dữ liệu từ các phân mảnh (Hà Đông, Cầu Giấy, Ngọc Trục)...")
    print(f"{'MÃ LỚP':<15} | {'TÊN MÔN HỌC':<20} | {'SĨ SỐ':<10} | {'CƠ SỞ':<10}")
    print("-" * 65)

    sites = ['HD', 'CG', 'NT']
    tong_so_lop = 0

    for site in sites:
        danh_sach = get_lop_toan_truong_site(site)
        for ma_lop_hp, ten_hp, so_luong_da_dang_ky, si_so_toi_da in danh_sach:
            si_so_str = f"{so_luong_da_dang_ky}/{si_so_toi_da}"
            print(f"{ma_lop_hp:<15} | {ten_hp:<20} | {si_so_str:<10} | {site:<10}")
            tong_so_lop += 1

    print("-" * 65)
    print(f"✅ Tổng cộng: {tong_so_lop} lớp học phần trên toàn hệ thống.\n")

if __name__ == "__main__":
    xem_danh_sach_lop_toan_truong()
