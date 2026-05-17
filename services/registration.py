# d:\BTL-CSDLPT\services\registration.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import hàm tương tác trực tiếp với Database từ lớp db
from db.transaction import execute_dang_ky_hoc_phan

def dang_ky_hoc_phan(ma_sv, ma_lop_hp, site_code):
    """
    Tầng Services (Xử lý nghiệp vụ): 
    Nơi này chỉ chứa các quy tắc kinh doanh (Business Logic).
    Tất cả các logic liên quan đến CSDL (Transaction, SQL, Rollback) đã được đẩy xuống tầng DB.
    """
    
    print(f"🔄 Bắt đầu xử lý quy trình đăng ký cho sinh viên {ma_sv} vào lớp {ma_lop_hp}...")
    
    # [BUSINESS LOGIC] 1. Kiểm tra tính hợp lệ của dữ liệu đầu vào (Validation)
    if not ma_sv or not ma_lop_hp or not site_code:
        print("❌ Lỗi nghiệp vụ: Thiếu thông tin đầu vào (Mã SV, Mã Lớp hoặc Cơ Sở).")
        return False
        
    # [BUSINESS LOGIC] 2. Định tuyến xuống tầng CSDL để thực hiện Transaction an toàn
    ket_qua = execute_dang_ky_hoc_phan(ma_sv, ma_lop_hp, site_code)
    
    # [BUSINESS LOGIC] 3. Xử lý sau khi đăng ký (nếu có)
    if ket_qua:
        # Ví dụ: Gửi email, ghi log hệ thống, thông báo webhook...
        # print(f"📧 Đã gửi email thông báo thành công tới {ma_sv}.")
        pass
        
    return ket_qua
