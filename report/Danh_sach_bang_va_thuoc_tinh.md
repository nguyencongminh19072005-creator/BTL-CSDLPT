# Danh sách Bảng và Thuộc tính trong Hệ thống

## 1. co_so (Cơ sở)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_co_so` | String(20), Primary Key |
| `ten_co_so` | String(100), Not Null |
| `dia_chi` | String(255) |

## 2. khoa (Khoa)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_khoa` | String(20), Primary Key |
| `ten_khoa` | String(100), Not Null |

## 3. sinh_vien (Sinh viên)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_sv` | String(20), Primary Key |
| `ho_ten` | String(100), Not Null |
| `ngay_sinh` | Date |
| `gioi_tinh` | String(10) |
| `ma_khoa` | String(20), Foreign Key (khoa.ma_khoa) |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |
| `da_xoa` | Boolean, Default=False |

## 4. giang_vien (Giảng viên)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_gv` | String(20), Primary Key |
| `ho_ten` | String(100), Not Null |
| `hoc_vi` | String(50) |
| `ma_khoa` | String(20), Foreign Key (khoa.ma_khoa) |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |
| `da_xoa` | Boolean, Default=False |

## 5. hoc_phan (Học phần)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_hp` | String(20), Primary Key |
| `ten_hp` | String(100), Not Null |
| `so_tin_chi` | Integer, Not Null |
| `ma_khoa` | String(20), Foreign Key (khoa.ma_khoa) |

## 6. phong_hoc (Phòng học)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_phong` | String(20), Primary Key |
| `ten_phong` | String(100), Not Null |
| `suc_chua` | Integer |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |

## 7. lop_hoc_phan (Lớp học phần)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_lop_hp` | String(20), Primary Key |
| `ma_hp` | String(20), Foreign Key (hoc_phan.ma_hp) |
| `ma_gv` | String(20) |
| `ma_phong` | String(20), Foreign Key (phong_hoc.ma_phong) |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |
| `hoc_ky` | Integer |
| `nam_hoc` | String(20) |
| `si_so_toi_da` | Integer |
| `so_luong_da_dang_ky` | Integer, Default=0 |
| `version` | Integer, Default=0, Not Null (Optimistic Locking) |

## 8. lich_hoc (Lịch học)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_lich` | String(20), Primary Key |
| `ma_lop_hp` | String(20), Foreign Key (lop_hoc_phan.ma_lop_hp) |
| `thu` | Integer |
| `tiet_bat_dau` | Integer |
| `tiet_ket_thuc` | Integer |
| `ma_phong` | String(20), Foreign Key (phong_hoc.ma_phong) |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |

## 9. dang_ky (Đăng ký)
| Tên thuộc tính | Định kiểu & Ràng buộc |
|---|---|
| `ma_dk` | Integer, Primary Key, Autoincrement |
| `ma_sv` | String(20), Not Null |
| `ma_lop_hp` | String(20), Foreign Key (lop_hoc_phan.ma_lop_hp) |
| `thoi_gian_dang_ky` | DateTime, Server Default=now() |
| `trang_thai` | String(50), Default='THANH_CONG' |
| `ma_co_so` | String(20), Foreign Key (co_so.ma_co_so) |

*Ràng buộc bổ sung: `UNIQUE(ma_sv, ma_lop_hp)` để tránh một sinh viên đăng ký cùng một lớp học phần nhiều lần.*
