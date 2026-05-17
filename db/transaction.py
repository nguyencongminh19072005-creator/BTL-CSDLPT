# d:\BTL-CSDLPT\db\transaction.py
import psycopg2
from db.config_db import get_connection
from db.query import (
    get_lop_hoc_phan,
    check_dang_ky,
    insert_dang_ky,
    update_lop_hoc_phan_version
)

def execute_dang_ky_hoc_phan(ma_sv, ma_lop_hp, site_code):
    """
    Quản lý toàn bộ giao dịch (Transaction) CSDL cho việc đăng ký học phần.
    Đảm bảo tính ACID và xử lý Optimistic Locking bằng SQL thuần.
    """
    conn = None
    cursor = None
    try:
        # Mở kết nối
        conn = get_connection(site_code)
        cursor = conn.cursor()
        
        # 1. Lấy thông tin lớp học phần (Sĩ số, Version)
        result = get_lop_hoc_phan(cursor, ma_lop_hp)
        
        if not result:
            print(f"❌ Lỗi: Không tìm thấy lớp học phần {ma_lop_hp} tại cơ sở {site_code}.")
            conn.rollback()
            return False
            
        si_so_toi_da, so_luong_da_dang_ky, current_version = result
        
        if so_luong_da_dang_ky >= si_so_toi_da:
            print(f"❌ Lỗi: Lớp học phần {ma_lop_hp} đã đủ sĩ số ({si_so_toi_da}).")
            conn.rollback()
            return False
            
        # 2. Kiểm tra sinh viên đã đăng ký chưa
        da_dang_ky = check_dang_ky(cursor, ma_sv, ma_lop_hp)
        
        if da_dang_ky:
            print(f"❌ Lỗi: Sinh viên {ma_sv} đã đăng ký lớp {ma_lop_hp} rồi.")
            conn.rollback()
            return False
            
        # 3. Insert bản ghi đăng ký mới
        try:
            insert_dang_ky(cursor, ma_sv, ma_lop_hp, site_code)
        except psycopg2.IntegrityError:
            conn.rollback()
            print(f"❌ Lỗi: Sinh viên {ma_sv} đã đăng ký lớp {ma_lop_hp} (Ràng buộc UNIQUE).")
            return False
            
        # 4. Cập nhật version (Optimistic Locking)
        rowcount = update_lop_hoc_phan_version(cursor, ma_lop_hp, current_version)
        
        if rowcount == 0:
            conn.rollback()
            print("❌ Lỗi: Trạng thái lớp học đã thay đổi bởi một giao dịch khác (Optimistic Locking). Vui lòng thử lại.")
            return False
            
        # Commit giao dịch
        conn.commit()
        print(f"✅ Đăng ký thành công! Sinh viên {ma_sv} đã được thêm vào lớp {ma_lop_hp} tại cơ sở {site_code}.")
        print(f"📊 Sĩ số mới của lớp: {so_luong_da_dang_ky + 1}/{si_so_toi_da}")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Lỗi DB Transaction: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
