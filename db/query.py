# d:\BTL-CSDLPT\db\query.py
from db.config_db import get_connection

# =====================================================================
# CÁC HÀM QUERY DÙNG CHUNG CURSOR (DÀNH CHO TRANSACTION NHIỀU BƯỚC)
# =====================================================================

def get_lop_hoc_phan(cursor, ma_lop_hp):
    """Lấy thông tin sĩ số và version hiện tại của lớp học phần."""
    query = """
        SELECT si_so_toi_da, so_luong_da_dang_ky, version 
        FROM lop_hoc_phan 
        WHERE ma_lop_hp = %s;
    """
    cursor.execute(query, (ma_lop_hp,))
    return cursor.fetchone()

def check_dang_ky(cursor, ma_sv, ma_lop_hp):
    """Kiểm tra xem sinh viên đã đăng ký lớp học phần này chưa."""
    query = """
        SELECT 1 
        FROM dang_ky 
        WHERE ma_sv = %s AND ma_lop_hp = %s;
    """
    cursor.execute(query, (ma_sv, ma_lop_hp))
    return cursor.fetchone()

def insert_dang_ky(cursor, ma_sv, ma_lop_hp, site_code):
    """Thêm mới một bản ghi đăng ký."""
    query = """
        INSERT INTO dang_ky (ma_sv, ma_lop_hp, ma_co_so) 
        VALUES (%s, %s, %s);
    """
    cursor.execute(query, (ma_sv, ma_lop_hp, site_code))

def update_lop_hoc_phan_version(cursor, ma_lop_hp, old_version):
    """Cập nhật sĩ số và version (Optimistic Locking)."""
    query = """
        UPDATE lop_hoc_phan 
        SET so_luong_da_dang_ky = so_luong_da_dang_ky + 1, 
            version = version + 1 
        WHERE ma_lop_hp = %s 
          AND version = %s;
    """
    cursor.execute(query, (ma_lop_hp, old_version))
    return cursor.rowcount  # Trả về số dòng được cập nhật


# =====================================================================
# CÁC HÀM QUERY TỰ QUẢN LÝ CONNECTION (DÀNH CHO ĐỌC DỮ LIỆU ĐỘC LẬP)
# =====================================================================

def get_lop_toan_truong_site(site_code):
    """Lấy danh sách tất cả lớp học phần tại một cơ sở."""
    query = """
        SELECT l.ma_lop_hp, hp.ten_hp, l.so_luong_da_dang_ky, l.si_so_toi_da
        FROM lop_hoc_phan l
        JOIN hoc_phan hp ON l.ma_hp = hp.ma_hp;
    """
    conn = None
    cursor = None
    try:
        conn = get_connection(site_code)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Lỗi truy xuất tại cơ sở {site_code}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
