# 🎓 Hệ thống Quản lý Đăng ký Học phần Phân tán (3 Sites)

Dự án môn học **Cơ sở dữ liệu phân tán (CSDLPT)** - Học viện Công nghệ Bưu chính Viễn thông (PTIT).  
Hệ thống được thiết kế để quản lý sinh viên, giảng viên, lớp học phần và nghiệp vụ đăng ký học phần trên mô hình cơ sở dữ liệu phân tán gồm 3 server (Nodes/Sites) kết hợp cơ chế kiểm soát giao dịch đồng thời bằng **Optimistic Locking (Khóa lạc quan)**.

---

## ⚡ HƯỚNG DẪN THIẾT LẬP NHANH (QUICK START - 5 BƯỚC)

Dành cho các thành viên trong nhóm thiết lập nhanh để chạy thử dự án trên máy cá nhân:

### 👉 Bước 1: Cài đặt công cụ nền tảng
*   **Python (Bản 3.8+):** [Tải và cài đặt tại đây](https://www.python.org/downloads/) (Nhớ tích chọn *Add Python to PATH* khi cài đặt).
*   **Docker Desktop:** [Tải và cài đặt tại đây](https://www.docker.com/products/docker-desktop/) (Dùng để dựng nhanh 3 cơ sở dữ liệu độc lập mà không cần cấu hình thủ công phức tạp).

### 👉 Bước 2: Cài đặt các thư viện Python hỗ trợ
Mở Terminal hoặc Command Prompt tại thư mục dự án `d:\BTL-CSDLPT` và chạy lệnh sau:
```bash
pip install sqlalchemy psycopg2-binary faker
```

### 👉 Bước 3: Khởi động 3 Server Database độc lập bằng Docker
Đảm bảo phần mềm **Docker Desktop đã được mở**, sau đó gõ lệnh sau trong Terminal dự án:
```bash
docker-compose up -d
```
> [!NOTE]
> Lệnh này sẽ tự động tải và dựng lên 3 database độc lập trên Docker:
> *   **Hà Đông** (Cổng `5435`)
> *   **Cầu Giấy** (Cổng `5433`)
> *   **Ngọc Trục** (Cổng `5434`)
> 
> Bạn có thể mở Docker Desktop lên thấy cả 3 container sáng đèn xanh lá cây là thành công.

### 👉 Bước 4: Tự động khởi tạo bảng & Bơm dữ liệu mẫu (Seeding)
Chạy duy nhất lệnh Python sau để tự động tạo cấu trúc CSDL và nạp dữ liệu kiểm thử tiếng Việt ngẫu nhiên (sử dụng thư viện Faker):
```bash
python db/seed_data.py
```
> [!IMPORTANT]
> Script này sẽ tự động xóa sạch dữ liệu cũ (nếu có), tạo lại **9 bảng** sạch sẽ và bơm dữ liệu phân mảnh tương ứng cho từng cơ sở, đồng thời thiết lập sẵn các dữ liệu đăng ký học phần chéo để test nghiệp vụ phân tán.

### 👉 Bước 5: Chạy chương trình và Kiểm thử
*   Để tương tác với **Menu hệ thống** (xem lớp mở toàn trường, thực hiện đăng ký học phần chéo cơ sở...), chạy lệnh:
    ```bash
    python main.py
    ```
*   Để chạy script kiểm thử **kiểm soát giao dịch đồng thời (Khóa lạc quan)** khi có 20-30 luồng bấm đăng ký cùng một tích tắc, chạy lệnh:
    ```bash
    python test/test_optimistic_locking.py
    ```

---

## 📌 1. Kiến trúc phân tán hệ thống

Hệ thống giả lập một cơ sở dữ liệu phân tán gồm 3 chi nhánh (Sites):
*   **Site 1: Hà Đông (HD)** - Trụ sở chính (Port: `5435`, DB Name: `qldt_hadong`)
*   **Site 2: Cầu Giấy (CG)** - Cơ sở phụ 1 (Port: `5433`, DB Name: `qldt_caugiay`)
*   **Site 3: Ngọc Trục (NT)** - Cơ sở phụ 2 (Port: `5434`, DB Name: `qldt_ngoctruc`)

### Chiến lược Phân tán & Lưu trữ:
1.  **Nhân bản hoàn toàn (Fully Replicated):** Các bảng danh mục chung ít thay đổi được nhân bản trên cả 3 Site để tăng tốc độ đọc dữ liệu:
    *   `co_so`, `khoa`, `hoc_phan`.
2.  **Phân mảnh ngang nguyên thủy (Horizontal Fragmentation):** Dữ liệu nghiệp vụ được phân mảnh ngang dựa trên thuộc tính vị trí (`ma_co_so`):
    *   `sinh_vien`, `giang_vien`, `phong_hoc`, `lop_hoc_phan`, `lich_hoc`, `dang_ky`.
3.  **Location Transparency (Trong suốt vị trí):** Hệ thống cho phép:
    *   Giảng viên cơ sở này dạy chéo tại cơ sở khác (ví dụ: GV Hà Đông dạy lớp ở Cầu Giấy).
    *   Sinh viên cơ sở này sang đăng ký học chéo lớp tại cơ sở khác.

---

## 🚀 2. Tính năng nổi bật & Giải pháp kỹ thuật

*   **Truy vấn phân tán (Distributed Queries):** Quét song song và hợp nhất dữ liệu từ tất cả các Site (Hà Đông, Cầu Giấy, Ngọc Trục) để hiển thị danh sách lớp học toàn trường mà không bị giới hạn địa lý.
*   **Kiểm soát đồng thời (Concurrency Control):** Áp dụng **Optimistic Locking (Khóa lạc quan)** bằng SQL thuần qua cột `version` trong bảng `lop_hoc_phan`. Đảm bảo khi hàng trăm sinh viên cùng đăng ký vào 1 lớp tại cùng 1 thời điểm, sĩ số không bao giờ vượt quá giới hạn và không xảy ra hiện tượng "Dirty Read" hay "Lost Update".
*   **Kiến trúc Phân lớp Sạch sẽ:**
    *   `db/model/`: Khai báo cấu trúc bảng (SQLAlchemy).
    *   `db/query.py`: Chứa các hàm SQL thuần tương tác trực tiếp với Database.
    *   `db/transaction.py`: Đảm bảo tính **ACID**, quản lý mở kết nối, Commit/Rollback giao dịch và xử lý xung đột khóa lạc quan.
    *   `services/`: Tầng nghiệp vụ (Business Logic) điều phối luồng dữ liệu.
    *   `main.py`: Giao diện dòng lệnh (CLI menu) thân thiện để tương tác.

---

## 🗂 3. Cấu trúc thư mục dự án

```text
d:\BTL-CSDLPT\
│
├── app/
│   └── main.py             # File khởi chạy ứng dụng (nếu có Web/API)
├── db/
│   ├── model/              # Thư mục chứa định nghĩa các bảng SQLAlchemy
│   ├── config_db.py        # Cấu hình kết nối tới 3 cơ sở (PostgreSQL)
│   ├── distributed_queries.py # Thực hiện các truy vấn phân tán toàn trường
│   ├── query.py            # Tổng hợp các hàm SQL thuần thao tác dữ liệu
│   ├── seed_data.py        # Kịch bản xóa sạch và tự động sinh dữ liệu mẫu
│   └── transaction.py      # Xử lý giao dịch Đăng ký (Optimistic Locking)
├── services/
│   └── registration.py     # Tầng nghiệp vụ xử lý logic đăng ký học phần
├── test/
│   ├── test_query.py       # Kiểm tra các câu truy vấn cơ bản
│   └── test_optimistic_locking.py # Script giả lập hàng chục luồng đăng ký đồng thời
├── docker-compose.yml      # Cấu hình khởi tạo nhanh 3 Server Postgres
├── requirements.txt        # Các thư viện Python cần cài đặt
├── main.py                 # File chạy chính của chương trình (Giao diện CLI)
└── README.md               # Tài liệu hướng dẫn sử dụng này
```

---

## 🤝 4. Quy ước làm việc nhóm (Teamwork Guidelines)

Để dự án không bị xung đột code và hoạt động trơn tru, các thành viên thống nhất các quy tắc sau:
1.  **Không viết logic DB ở tầng UI/Service:**
    *   Tất cả các câu lệnh SQL thuần (`SELECT`, `INSERT`, `UPDATE`) phải được viết trong [db/query.py](file:///d:/BTL-CSDLPT/db/query.py).
    *   Tầng dịch vụ [services/](file:///d:/BTL-CSDLPT/services) chỉ điều hướng và xử lý nghiệp vụ chung.
2.  **Sử dụng Transaction an toàn:**
    *   Mọi thao tác thay đổi dữ liệu (`INSERT`, `UPDATE`, `DELETE`) bắt buộc phải thực hiện trong khối `try-except` và có lệnh `conn.rollback()` khi xảy ra lỗi để tránh khóa bảng hay sai lệch dữ liệu phân tán.
3.  **Tôn trọng cấu trúc phân mảnh:**
    *   Khi thêm mới một dữ liệu phân mảnh (Sinh viên, Giảng viên,...), phải đảm bảo dữ liệu đó được lưu đúng vào Database của chi nhánh (Site) chứa nó dựa trên thuộc tính `ma_co_so`.