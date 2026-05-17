# Danh sách Quan hệ giữa các Lớp (Bảng) trong Hệ thống

Dưới đây là danh sách mô tả các mối quan hệ logic và ràng buộc khóa ngoại (Foreign Key) giữa các bảng trong hệ thống CSDL Phân tán.

## 1. Quan hệ từ `co_so` (Cơ sở)
Cơ sở là bảng trung tâm phân mảnh dữ liệu. Hầu hết các thực thể đều phụ thuộc vào một cơ sở nhất định (Quan hệ **1-N**):
- **1 Cơ sở - N Sinh viên**: Một cơ sở quản lý nhiều sinh viên (`sinh_vien.ma_co_so` tham chiếu tới `co_so.ma_co_so`).
- **1 Cơ sở - N Giảng viên**: Một cơ sở quản lý nhiều giảng viên (`giang_vien.ma_co_so` tham chiếu tới `co_so.ma_co_so`).
- **1 Cơ sở - N Phòng học**: Một cơ sở sở hữu nhiều phòng học (`phong_hoc.ma_co_so` tham chiếu tới `co_so.ma_co_so`).
- **1 Cơ sở - N Lớp học phần**: Một cơ sở mở nhiều lớp học phần (`lop_hoc_phan.ma_co_so` tham chiếu tới `co_so.ma_co_so`).
- **1 Cơ sở - N Lịch học**: Quản lý lịch học thuộc cơ sở nào (`lich_hoc.ma_co_so` tham chiếu tới `co_so.ma_co_so`).
- **1 Cơ sở - N Đăng ký**: Quản lý phiếu đăng ký phát sinh tại cơ sở nào (`dang_ky.ma_co_so` tham chiếu tới `co_so.ma_co_so`).

## 2. Quan hệ từ `khoa` (Khoa)
Quản lý các thực thể trực thuộc quản lý của Khoa (Quan hệ **1-N**):
- **1 Khoa - N Sinh viên**: Sinh viên thuộc về một khoa (`sinh_vien.ma_khoa` tham chiếu tới `khoa.ma_khoa`).
- **1 Khoa - N Giảng viên**: Giảng viên công tác tại một khoa (`giang_vien.ma_khoa` tham chiếu tới `khoa.ma_khoa`).
- **1 Khoa - N Học phần**: Môn học (Học phần) do một khoa chịu trách nhiệm quản lý (`hoc_phan.ma_khoa` tham chiếu tới `khoa.ma_khoa`).

## 3. Quan hệ từ `hoc_phan` (Học phần)
- **1 Học phần - N Lớp học phần**: Mỗi môn học (Học phần) có thể được mở thành nhiều Lớp học phần khác nhau trong các học kỳ (`lop_hoc_phan.ma_hp` tham chiếu tới `hoc_phan.ma_hp`).

## 4. Quan hệ từ `phong_hoc` (Phòng học)
- **1 Phòng học - N Lớp học phần**: Một lớp học phần có thể được gán một phòng học mặc định (`lop_hoc_phan.ma_phong` tham chiếu tới `phong_hoc.ma_phong`).
- **1 Phòng học - N Lịch học**: Mỗi phòng học sẽ được xếp cho nhiều lịch học/buổi học khác nhau (`lich_hoc.ma_phong` tham chiếu tới `phong_hoc.ma_phong`).

## 5. Quan hệ từ `lop_hoc_phan` (Lớp học phần)
Lớp học phần là thực thể trọng tâm của quy trình đào tạo:
- **1 Lớp học phần - N Lịch học**: Mỗi lớp học phần có thể có nhiều lịch học/buổi học khác nhau trong tuần (`lich_hoc.ma_lop_hp` tham chiếu tới `lop_hoc_phan.ma_lop_hp`).
- **1 Lớp học phần - N Đăng ký**: Một lớp học phần sẽ có nhiều sinh viên đăng ký tham gia (`dang_ky.ma_lop_hp` tham chiếu tới `lop_hoc_phan.ma_lop_hp`).

## 6. Các quan hệ logic đặc biệt (Không dùng Foreign Key cứng)
Do đặc thù của Cơ sở dữ liệu phân tán (Sinh viên/Giảng viên có thể thuộc site này nhưng thao tác trên site kia), một số quan hệ được thiết kế dưới dạng **Tham chiếu Logic** thay vì Khóa ngoại vật lý để tránh lỗi liên kết chéo site:
- **1 Sinh viên - N Đăng ký**: Một sinh viên đăng ký nhiều lớp. Bảng `dang_ky` lưu `ma_sv` nhưng không setup `ForeignKey('sinh_vien.ma_sv')` để hỗ trợ sinh viên site này có thể đăng ký lớp của site khác một cách trơn tru.
- **1 Giảng viên - N Lớp học phần**: Một giảng viên giảng dạy nhiều lớp. Bảng `lop_hoc_phan` lưu `ma_gv` nhưng không setup `ForeignKey('giang_vien.ma_gv')` để hỗ trợ việc giảng viên của cơ sở 1 có thể qua cơ sở 2 giảng dạy.

---
> **Lưu ý mô hình ERD**: Hầu hết các quan hệ trong thiết kế này đều là quan hệ Một-Nhiều (1-N). Quan hệ Nhiều-Nhiều (N-N) giữa `sinh_vien` và `lop_hoc_phan` đã được chuẩn hóa và tách ra thành bảng trung gian là `dang_ky`.
