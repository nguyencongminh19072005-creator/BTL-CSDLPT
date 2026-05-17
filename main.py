import sys
sys.stdout.reconfigure(encoding='utf-8')

from db.distributed_queries import xem_danh_sach_lop_toan_truong
from services.registration import dang_ky_hoc_phan

def menu():
    while True:
        print("\n" + "="*50)
        print("🎓 HỆ THỐNG ĐĂNG KÝ HỌC PHẦN PHÂN TÁN")
        print("="*50)
        print("1. Xem danh sách lớp mở (Truy vấn phân tán)")
        print("2. Đăng ký học phần")
        print("0. Thoát")
        
        chon = input("Chọn chức năng (0-2): ")
        
        if chon == '1':
            xem_danh_sach_lop_toan_truong()
        elif chon == '2':
            print("\n--- NHẬP THÔNG TIN ĐĂNG KÝ ---")
            site = input("Cơ sở muốn thao tác (HD/CG/NT): ").upper()
            sv = input("Mã sinh viên (VD: SV_HD_001): ").upper()
            lhp = input("Mã lớp học phần (VD: LHP_HD_01): ").upper()
            
            print("\n⏳ Đang xử lý giao dịch...")
            dang_ky_hoc_phan(ma_sv=sv, ma_lop_hp=lhp, site_code=site)
        elif chon == '0':
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    menu()
