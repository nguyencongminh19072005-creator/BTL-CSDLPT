import sys
import os
import threading
import time
import psycopg2

# Thêm đường dẫn để import các module của dự án (Lùi lại 1 cấp để trỏ về root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.config_db import get_connection
from db.query import (
    get_lop_hoc_phan,
    insert_dang_ky,
    update_lop_hoc_phan_version
)

def dang_ky_hoc_phan_cham(ma_sv, ma_lop_hp, site_code, delay=2):
    print(f"\n[{ma_sv}] Đang cố gắng đăng ký lớp {ma_lop_hp}...")
    
    conn = None
    cursor = None
    try:
        # Lấy connection psycopg2 thuần từ config
        conn = get_connection(site_code)
        cursor = conn.cursor()
        
        # Bước 1: Lấy thông tin bằng hàm query
        result = get_lop_hoc_phan(cursor, ma_lop_hp)
        if not result:
            print(f"[{ma_sv}] Không tìm thấy lớp học phần.")
            conn.rollback()
            return False
            
        si_so_toi_da, so_luong_da_dang_ky, current_version = result
        print(f"[{ma_sv}] Đã đọc được version: {current_version}, sĩ số hiện tại: {so_luong_da_dang_ky}")
        
        # Bước 2: Thêm bản ghi đăng ký mới (dùng hàm query)
        try:
            insert_dang_ky(cursor, ma_sv, ma_lop_hp, site_code)
        except psycopg2.IntegrityError:
            conn.rollback()
            print(f"❌ [{ma_sv}] Lỗi IntegrityError (Đã đăng ký trước đó rồi).")
            return False
        
        print(f"[{ma_sv}] Chuẩn bị commit, giả lập trễ {delay} giây để chờ luồng khác...")
        time.sleep(delay)
        
        # Bước 3: UPDATE để tăng sĩ số và version (Optimistic Locking bằng hàm query)
        rowcount = update_lop_hoc_phan_version(cursor, ma_lop_hp, current_version)
        
        if rowcount == 0:
            conn.rollback()
            print(f"❌ [{ma_sv}] Bắt được LỖI ĐỒNG THỜI! Trạng thái lớp học đã thay đổi bởi luồng khác.")
            return False
            
        conn.commit()
        print(f"✅ [{ma_sv}] Giao dịch THÀNH CÔNG! (Đã ghi đè lên DB bằng SQL thuần)")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ [{ma_sv}] Lỗi không xác định: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def run_test():
    site_code = "HD"
    
    # Bạn có thể thay "LHP_HD_01" bằng một mã Lớp Học Phần có thật trong CSDL của bạn
    ma_lop_hp = "LHP_HD_01" 
    
    print("=== BẮT ĐẦU GIẢ LẬP ĐĂNG KÝ ĐỒNG THỜI ===")
    
    # Giả lập 2 sinh viên bấm nút đăng ký cùng một lúc
    t1 = threading.Thread(target=dang_ky_hoc_phan_cham, args=("SV_HD_001", ma_lop_hp, site_code, 2))
    t2 = threading.Thread(target=dang_ky_hoc_phan_cham, args=("SV_HD_002", ma_lop_hp, site_code, 2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("\n=== KẾT THÚC TEST ===")

if __name__ == "__main__":
    run_test()
