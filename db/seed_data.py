import sys
import os
import random
from datetime import timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from faker import Faker
from config_db import engines, SessionLocals as SessionLocal
from model import Base, CoSo, Khoa, HocPhan, SinhVien, GiangVien, PhongHoc, LopHocPhan, LichHoc, DangKy

# Khởi tạo Faker tiếng Việt
fake = Faker('vi_VN')

def reset_dbs():
    """Hàm này xóa sạch cấu trúc cũ và tạo lại để đảm bảo quá trình test seed data không bị trùng lặp"""
    print("Dang xoa toan bo cau truc va du lieu cu tren 3 Server...")
    for site, engine in engines.items():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print(f"  -> Đã Reset thành công Server {site}")

def seed_data():
    reset_dbs()
    
    print("\nBat dau tao du lieu mau...")
    
    dbs = {
        'HD': SessionLocal['HD'](),
        'CG': SessionLocal['CG'](),
        'NT': SessionLocal['NT']()
    }
    
    # =========================================================
    # 1. DỮ LIỆU NHÂN BẢN (REPLICATED)
    # =========================================================
    print("\n[1/2] Đang tạo dữ liệu Nhân bản (Cơ sở, Khoa, Học phần)...")
    
    cosos_data = [
        {"ma_co_so": "HD", "ten_co_so": "Cơ sở Hà Đông", "dia_chi": "Hà Đông, Hà Nội"},
        {"ma_co_so": "CG", "ten_co_so": "Cơ sở Cầu Giấy", "dia_chi": "Cầu Giấy, Hà Nội"},
        {"ma_co_so": "NT", "ten_co_so": "Cơ sở Ngọc Trục", "dia_chi": "Ngọc Trục, Nam Định"}
    ]
    
    khoas_data = [
        {"ma_khoa": "CNTT", "ten_khoa": "Công nghệ Thông tin"},
        {"ma_khoa": "VT", "ten_khoa": "Viễn thông"},
        {"ma_khoa": "KT", "ten_khoa": "Kế toán"},
        {"ma_khoa": "PT", "ten_khoa": "Đa phương tiện"}
    ]
    
    hocphans_data = [
        {"ma_hp": "INT101", "ten_hp": "Lập trình C++", "so_tin_chi": 3, "ma_khoa": "CNTT"},
        {"ma_hp": "INT102", "ten_hp": "Cơ sở dữ liệu", "so_tin_chi": 3, "ma_khoa": "CNTT"},
        {"ma_hp": "INT103", "ten_hp": "CSDL Phân tán", "so_tin_chi": 3, "ma_khoa": "CNTT"},
        {"ma_hp": "TEL201", "ten_hp": "Mạng viễn thông", "so_tin_chi": 3, "ma_khoa": "VT"},
        {"ma_hp": "PT101", "ten_hp": "Thiết kế Đồ họa", "so_tin_chi": 3, "ma_khoa": "PT"}
    ]

    for site_code, db in dbs.items():
        try:
            for item in cosos_data: db.add(CoSo(**item))
            db.commit()
            for item in khoas_data: db.add(Khoa(**item))
            db.commit()
            for item in hocphans_data: db.add(HocPhan(**item))
            db.commit()
            print(f"  -> Đã nhân bản danh mục thành công tại Node {site_code}")
        except Exception as e:
            db.rollback()
            print(f"  Loi tao danh muc tai Node {site_code}: {e}")

    # =========================================================
    # 2. DỮ LIỆU PHÂN MẢNH VÀ NGHIỆP VỤ (Sinh viên, GV, Đăng ký, Lịch học)
    # =========================================================
    print("\n[2/2] Đang tạo dữ liệu Phân mảnh (Kèm tính năng Location Transparency)...")
    
    for site_code, db in dbs.items():
        print(f"  -> Bơm dữ liệu riêng cho Node {site_code}...")
        try:
            # Tạo Phòng học
            phonghocs = []
            for i in range(1, 6):
                phong = PhongHoc(ma_phong=f"P_{site_code}_{i}", ten_phong=f"Phòng {i} - {site_code}", suc_chua=50, ma_co_so=site_code)
                phonghocs.append(phong)
                db.add(phong)
            db.commit()
                
            # Tạo Giảng viên
            giangviens = []
            for i in range(1, 11):
                gv = GiangVien(
                    ma_gv=f"GV_{site_code}_{i:02d}",
                    ho_ten=fake.name(),
                    hoc_vi=random.choice(["Thạc sĩ", "Tiến sĩ", "PGS"]),
                    ma_khoa=random.choice(khoas_data)["ma_khoa"],
                    ma_co_so=site_code
                )
                giangviens.append(gv)
                db.add(gv)
            db.commit()
                
            # Tạo Sinh viên
            sinhviens = []
            for i in range(1, 51):
                sv = SinhVien(
                    ma_sv=f"SV_{site_code}_{i:03d}",
                    ho_ten=fake.name(),
                    ngay_sinh=fake.date_of_birth(minimum_age=18, maximum_age=25),
                    gioi_tinh=random.choice(["Nam", "Nữ"]),
                    ma_khoa=random.choice(khoas_data)["ma_khoa"],
                    ma_co_so=site_code
                )
                sinhviens.append(sv)
                db.add(sv)
            db.commit()
                
            # Tạo Lớp học phần
            lhp_list = []
            for i in range(1, 11):
                # Demo Giảng viên dạy chéo (Location Transparency)
                # Có 20% khả năng một lớp ở CG hoặc NT sẽ do giáo viên "GV_HD_01" (Hà Đông) sang dạy
                if site_code != 'HD' and random.random() < 0.2:
                    ma_gv_chon = "GV_HD_01"
                else:
                    ma_gv_chon = random.choice(giangviens).ma_gv

                lhp = LopHocPhan(
                    ma_lop_hp=f"LHP_{site_code}_{i:02d}",
                    ma_hp=random.choice(hocphans_data)["ma_hp"],
                    ma_gv=ma_gv_chon,
                    ma_phong=random.choice(phonghocs).ma_phong,
                    ma_co_so=site_code,
                    hoc_ky=1,
                    nam_hoc="2026-2027",
                    si_so_toi_da=50,
                    so_luong_da_dang_ky=0
                )
                lhp_list.append(lhp)
                db.add(lhp)
            db.commit()

            # Tạo Lịch Học
            for lhp in lhp_list:
                lich = LichHoc(
                    ma_lich=f"LICH_{lhp.ma_lop_hp}",
                    ma_lop_hp=lhp.ma_lop_hp,
                    thu=random.randint(2, 7),
                    tiet_bat_dau=random.choice([1, 4, 7, 10]),
                    tiet_ket_thuc=random.choice([3, 6, 9, 12]),
                    ma_phong=lhp.ma_phong,
                    ma_co_so=site_code
                )
                db.add(lich)
            db.commit()

            # Tạo Đăng ký học phần (Location Transparency cho Sinh viên học chéo)
            for lhp in lhp_list:
                # Mỗi lớp chọn ngẫu nhiên 3-5 sinh viên thuộc cơ sở này đăng ký
                sv_dk_list = random.sample(sinhviens, random.randint(3, 5))
                for sv in sv_dk_list:
                    dk = DangKy(ma_sv=sv.ma_sv, ma_lop_hp=lhp.ma_lop_hp, ma_co_so=site_code)
                    db.add(dk)
                    lhp.so_luong_da_dang_ky += 1
                
                # Cố tình đưa 1 sinh viên Hà Đông (SV_HD_001) sang đăng ký học chéo tại CG hoặc NT
                if site_code != 'HD':
                    dk_cheo = DangKy(ma_sv="SV_HD_001", ma_lop_hp=lhp.ma_lop_hp, ma_co_so=site_code)
                    db.add(dk_cheo)
                    lhp.so_luong_da_dang_ky += 1

            db.commit()
            print(f"  Da sinh xong du lieu phan manh (kem Lich Hoc va Dang ky) cho Node {site_code}")
        except Exception as e:
            db.rollback()
            print(f"  Loi phan manh tai Node {site_code}: {e}")

    for db in dbs.values():
        db.close()
        
    print("\nHOAN TAT TOAN BO QUY TRINH SEED DATA!")

if __name__ == "__main__":
    seed_data()
