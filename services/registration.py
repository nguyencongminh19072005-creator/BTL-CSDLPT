import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from db.config_db import SessionLocals
from db.model import LopHocPhan, DangKy

def dang_ky_hoc_phan(ma_sv, ma_lop_hp, site_code):
    if site_code not in SessionLocals:
        print(f"❌ Lỗi: Cơ sở {site_code} không hợp lệ.")
        return False

    session = SessionLocals[site_code]()
    try:
        # Lấy thông tin lớp học phần
        lop_hp = session.query(LopHocPhan).filter(LopHocPhan.ma_lop_hp == ma_lop_hp).first()
        if not lop_hp:
            print(f"❌ Lỗi: Không tìm thấy lớp học phần {ma_lop_hp} tại cơ sở {site_code}.")
            return False
            
        if lop_hp.so_luong_da_dang_ky >= lop_hp.si_so_toi_da:
            print(f"❌ Lỗi: Lớp học phần {ma_lop_hp} đã đủ sĩ số ({lop_hp.si_so_toi_da}).")
            return False

        # Kiểm tra xem sinh viên đã đăng ký chưa
        da_dang_ky = session.query(DangKy).filter(
            DangKy.ma_sv == ma_sv,
            DangKy.ma_lop_hp == ma_lop_hp
        ).first()
        
        if da_dang_ky:
            print(f"❌ Lỗi: Sinh viên {ma_sv} đã đăng ký lớp {ma_lop_hp} rồi.")
            return False

        # Tạo bản ghi đăng ký mới
        dk_moi = DangKy(ma_sv=ma_sv, ma_lop_hp=ma_lop_hp, ma_co_so=site_code)
        session.add(dk_moi)
        
        # Tăng sĩ số và cập nhật version (Optimistic Locking)
        lop_hp.so_luong_da_dang_ky += 1
        lop_hp.version += 1
        
        session.commit()
        print(f"✅ Đăng ký thành công! Sinh viên {ma_sv} đã được thêm vào lớp {ma_lop_hp} tại cơ sở {site_code}.")
        print(f"📊 Sĩ số mới của lớp: {lop_hp.so_luong_da_dang_ky}/{lop_hp.si_so_toi_da}")
        return True

    except IntegrityError:
        session.rollback()
        print(f"❌ Lỗi: Sinh viên {ma_sv} đã đăng ký lớp {ma_lop_hp} (Ràng buộc UNIQUE).")
        return False
    except StaleDataError:
        session.rollback()
        print(f"❌ Lỗi: Trạng thái lớp học đã thay đổi bởi một giao dịch khác (Optimistic Locking). Vui lòng thử lại.")
        return False
    except Exception as e:
        session.rollback()
        print(f"❌ Lỗi hệ thống: {e}")
        return False
    finally:
        session.close()
