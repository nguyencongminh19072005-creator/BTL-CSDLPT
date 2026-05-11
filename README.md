# 🎓 Hệ thống Quản lý Đăng ký Học phần Phân tán (3 Sites)

Dự án môn học **Cơ sở dữ liệu phân tán** - Học viện Công nghệ Bưu chính Viễn thông (PTIT).

## 📌 Tổng quan dự án
Hệ thống được thiết kế để quản lý sinh viên, giảng viên, lớp học phần và nghiệp vụ đăng ký học phần trên mô hình cơ sở dữ liệu phân tán gồm 3 server (Sites):
- **Site 1: Hà Đông (HD)** - Cổng 5435
- **Site 2: Cầu Giấy (CG)** - Cổng 5433
- **Site 3: Trục Ngọc (TN)** - Cổng 5434

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.x
- **Cơ sở dữ liệu:** PostgreSQL (Triển khai trên Docker)
- **ORM:** SQLAlchemy (Quản lý Model và kết nối)
- **Thư viện bổ sung:** `psycopg2-binary`, `Faker` (tạo dữ liệu mẫu).

## 🗂 Cấu trúc Cơ sở dữ liệu (9 Bảng)
Hệ thống áp dụng các kỹ thuật phân tán:
1. **Nhân bản (Replicated):** `co_so`, `khoa`, `hoc_phan`.
2. **Phân mảnh ngang (Fragmented):** `sinh_vien`, `giang_vien`, `phong_hoc`, `lop_hoc_phan`, `lich_hoc`, `dang_ky`.



## 🚀 Hướng dẫn cài đặt & Chạy dự án

### 1. Chuẩn bị môi trường
Cài đặt các thư viện cần thiết:
```bash
pip install sqlalchemy psycopg2-binary faker