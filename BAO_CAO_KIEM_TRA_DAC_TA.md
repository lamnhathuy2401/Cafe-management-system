# BÁO CÁO KIỂM TRA HỆ THỐNG SO VỚI ĐẶC TẢ

## TỔNG QUAN
Báo cáo này đánh giá mức độ tuân thủ của hệ thống Coffee Manager với các Use Case đã được đặc tả.

---

## I. USE CASE CHUNG DÀNH CHO CÁC TÁC NHÂN

### ✅ UC-00: Đăng nhập
**Trạng thái:** ⚠️ **CHƯA ĐÚNG ĐẶC TẢ**

**Vấn đề:**
- ❌ Đặc tả yêu cầu đăng nhập bằng **Số điện thoại**, nhưng hệ thống hiện tại dùng **Email**
- ✅ Có xác thực mật khẩu
- ✅ Có tạo session
- ✅ Có chuyển hướng theo vai trò
- ✅ Có xử lý lỗi khi tài khoản không tồn tại hoặc sai mật khẩu

**Cần sửa:**
- Thay đổi trường đăng nhập từ Email sang Số điện thoại
- Cập nhật validation và tìm kiếm user theo phone thay vì email

---

### ⚠️ UC-001: Khôi phục mật khẩu
**Trạng thái:** ⚠️ **CHƯA ĐÚNG ĐẶC TẢ**

**Vấn đề:**
- ❌ Đặc tả yêu cầu xác minh qua **Số điện thoại** và gửi **OTP**
- ✅ Hiện tại có chức năng khôi phục mật khẩu nhưng dùng **Email** và **Token** (không phải OTP)
- ❌ Không có bước xác minh OTP
- ❌ Không có chức năng "Gửi lại mã OTP"

**Cần sửa:**
- Thay đổi từ Email sang Số điện thoại
- Tích hợp hệ thống gửi OTP qua SMS
- Thêm bước xác minh OTP
- Thêm chức năng gửi lại OTP

---

## II. USE CASE DÀNH CHO VAI TRÒ KHÁCH HÀNG

### ⚠️ UC-01: Đăng ký tài khoản
**Trạng thái:** ⚠️ **CHƯA ĐÚNG ĐẶC TẢ**

**Vấn đề:**
- ❌ Đặc tả yêu cầu **Số điện thoại làm tên đăng nhập**, nhưng hệ thống dùng Email
- ✅ Có validation mật khẩu và nhập lại mật khẩu
- ✅ Có kiểm tra số điện thoại đã tồn tại
- ✅ Có tự động đăng nhập sau khi đăng ký (theo đặc tả bước 7)

**Cần sửa:**
- Thay đổi trường đăng nhập chính từ Email sang Số điện thoại
- Email có thể là trường tùy chọn

---

### ✅ UC-02: Đặt món
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Xem menu theo danh mục
- ✅ Hiển thị giá và trạng thái (còn hàng/hết hàng)
- ✅ Thêm món vào giỏ hàng
- ✅ Xem giỏ hàng với chi tiết
- ✅ Tạo đơn hàng với trạng thái "Chờ xác nhận"
- ✅ Làm rỗng giỏ hàng sau khi đặt hàng
- ✅ Xử lý trường hợp giỏ hàng rỗng

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ✅ UC-03: Thanh toán đơn hàng
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Xem chi tiết đơn hàng chờ thanh toán
- ✅ Chọn phương thức thanh toán (Ví điện tử, Thẻ ngân hàng, Thanh toán tại quầy)
- ✅ Cập nhật trạng thái đơn hàng sau thanh toán
- ✅ Xử lý trường hợp "Thanh toán tại quầy"
- ✅ Xử lý lỗi giao dịch

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ⚠️ UC-04: Đặt bàn trước
**Trạng thái:** ⚠️ **CHƯA CÓ API BACKEND**

**Vấn đề:**
- ✅ Có UI form đặt bàn (ngày, giờ, số lượng người, ghi chú)
- ❌ **Chưa có API endpoint** để lưu reservation vào database
- ❌ Chưa có kiểm tra bàn trống vào thời điểm yêu cầu
- ❌ Chưa có thông báo cho nhân viên khi có đặt bàn mới

**Cần thêm:**
- API endpoint `/api/create-reservation` để tạo reservation
- API endpoint `/api/reservations` để lấy danh sách reservations
- Logic kiểm tra bàn trống dựa trên thời gian và số lượng người
- Cập nhật trạng thái bàn khi có reservation

---

### ✅ UC-05: Gửi phản hồi và đánh giá
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Form gửi phản hồi với đánh giá (sao)
- ✅ Nhập nội dung phản hồi
- ✅ Lưu phản hồi vào database
- ✅ Validation nội dung không được bỏ trống
- ✅ API endpoint `/api/submit-feedback`

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

## III. USE CASE DÀNH CHO VAI TRÒ NHÂN VIÊN

### ✅ UC-06: Tạo và quản lý đơn hàng (Tại quầy)
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Giao diện POS để tạo đơn hàng
- ✅ Chọn món và số lượng
- ✅ Áp dụng mã khuyến mãi
- ✅ Nhập số điện thoại khách hàng để tích điểm
- ✅ Tạo đơn hàng với trạng thái "Chờ thanh toán"
- ✅ API endpoint `/api/create-order`

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ✅ UC-07: Cập nhật trạng thái đơn hàng
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Xem danh sách đơn hàng
- ✅ Cập nhật trạng thái (pending → in_preparation → completed)
- ✅ API endpoint `/api/update-order-status`
- ✅ Hiển thị thông báo khi cập nhật

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ✅ UC-08: Xử lý thanh toán (Tại quầy)
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Chọn đơn hàng cần thanh toán
- ✅ Hỗ trợ 3 phương thức: Tiền mặt, Thẻ ngân hàng, Ví điện tử
- ✅ Tính tiền thối lại cho tiền mặt
- ✅ Hiển thị QR code cho ví điện tử
- ✅ Cập nhật trạng thái đơn hàng sau thanh toán
- ✅ API endpoint `/api/process-payment`

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ✅ UC-09: Chấm công
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Chức năng "Vào ca" (clock_in)
- ✅ Chức năng "Ra ca" (clock_out)
- ✅ Tính tổng thời gian làm việc
- ✅ Kiểm tra đã vào ca trước khi ra ca
- ✅ Kiểm tra đã vào ca trước khi vào ca lại
- ✅ Lưu vào attendance.csv
- ✅ API endpoint `/api/clock-in-out`
- ✅ API endpoint `/api/attendance` để xem lịch sử

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ⚠️ UC-10: Quản lý bàn
**Trạng thái:** ⚠️ **CHƯA ĐẦY ĐỦ**

**Đã có:**
- ✅ Hiển thị danh sách bàn với trạng thái
- ✅ API endpoint `/api/tables` để lấy danh sách bàn

**Thiếu:**
- ❌ Chưa có API endpoint để cập nhật trạng thái bàn
- ❌ Chưa có chức năng "Gán khách vào bàn"
- ❌ Chưa có chức năng "Dọn bàn" (clear table)
- ❌ Chưa có chức năng "Khách đã đến" cho reservation

**Cần thêm:**
- API endpoint `/api/update-table-status` để cập nhật trạng thái bàn
- API endpoint `/api/assign-table-to-order` để gán bàn cho đơn hàng
- Logic tự động cập nhật trạng thái bàn khi tạo đơn hàng

---

### ✅ UC-11: Kiểm kê kho
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Form kiểm kê kho với danh sách nguyên liệu
- ✅ Nhập số lượng thực tế
- ✅ Tính chênh lệch
- ✅ Nhập lý do chênh lệch
- ✅ Cập nhật tồn kho hệ thống
- ✅ API endpoint `/api/inventory-check`

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ⚠️ UC-12: Báo cáo ca làm
**Trạng thái:** ⚠️ **CHƯA CÓ API BACKEND**

**Đã có:**
- ✅ UI form báo cáo ca làm
- ✅ Hiển thị thống kê (số đơn hàng, doanh thu)
- ✅ Form nhập tiền mặt thực tế
- ✅ Form nhập ghi chú

**Thiếu:**
- ❌ **Chưa có API endpoint** để lưu báo cáo ca
- ❌ Chưa có kiểm tra đơn hàng chưa hoàn tất trước khi chốt ca
- ❌ Chưa có tính toán chênh lệch tiền mặt
- ❌ Chưa có in biên nhận chốt ca

**Cần thêm:**
- API endpoint `/api/shift-report` để lưu báo cáo ca
- Logic kiểm tra đơn hàng chưa hoàn tất
- Tính toán và hiển thị chênh lệch tiền mặt
- Tạo bản ghi báo cáo ca trong database

---

## IV. USE CASE DÀNH CHO VAI TRÒ QUẢN LÝ

### ⚠️ UC-13: Quản lý menu
**Trạng thái:** ⚠️ **CHƯA CÓ API BACKEND**

**Đã có:**
- ✅ UI để xem danh sách menu items
- ✅ UI form thêm món mới
- ✅ UI form sửa món
- ✅ UI nút xóa món

**Thiếu:**
- ❌ **Chưa có API endpoint** để thêm menu item
- ❌ **Chưa có API endpoint** để sửa menu item
- ❌ **Chưa có API endpoint** để xóa/ẩn menu item
- ❌ Chưa có validation (giá phải là số, tên không được trống)
- ❌ Chưa có kiểm tra món đã có lịch sử bán hàng trước khi xóa

**Cần thêm:**
- API endpoint `/api/menu-items` (POST) để thêm món
- API endpoint `/api/menu-items/{id}` (PUT) để sửa món
- API endpoint `/api/menu-items/{id}` (DELETE) để xóa/ẩn món
- Validation và kiểm tra lịch sử bán hàng

---

### ⚠️ UC-14: Tạo chương trình khuyến mãi
**Trạng thái:** ⚠️ **CHƯA CÓ API BACKEND**

**Đã có:**
- ✅ UI để xem danh sách promotions
- ✅ UI form tạo promotion mới

**Thiếu:**
- ❌ **Chưa có API endpoint** để tạo promotion
- ❌ **Chưa có API endpoint** để sửa promotion
- ❌ **Chưa có API endpoint** để xóa promotion
- ❌ Chưa có validation (mã code không được trùng, thời gian hợp lệ)

**Cần thêm:**
- API endpoint `/api/promotions` (POST) để tạo promotion
- API endpoint `/api/promotions/{id}` (PUT) để sửa promotion
- API endpoint `/api/promotions/{id}` (DELETE) để xóa promotion
- Validation mã code và thời gian

---

### ⚠️ UC-15: Quản lý nhân viên và khách hàng
**Trạng thái:** ⚠️ **CHƯA CÓ API BACKEND**

**Đã có:**
- ✅ UI để xem danh sách nhân viên
- ✅ UI để xem danh sách khách hàng
- ✅ UI form thêm nhân viên mới
- ✅ UI để xem phản hồi của khách hàng

**Thiếu:**
- ❌ **Chưa có API endpoint** để tạo tài khoản nhân viên
- ❌ **Chưa có API endpoint** để cập nhật thông tin/quyền nhân viên
- ❌ **Chưa có API endpoint** để reset mật khẩu khách hàng
- ❌ **Chưa có API endpoint** để trả lời phản hồi
- ❌ Chưa có hệ thống phân quyền (Thu ngân, Pha chế, Phục vụ)

**Cần thêm:**
- API endpoint `/api/staff` (POST) để tạo nhân viên
- API endpoint `/api/staff/{id}` (PUT) để cập nhật nhân viên
- API endpoint `/api/customers/{id}/reset-password` để reset mật khẩu
- API endpoint `/api/feedback/{id}/respond` để trả lời phản hồi
- Hệ thống phân quyền dựa trên role

---

### ✅ UC-16: Xem báo cáo doanh thu, thống kê
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Dashboard hiển thị doanh thu tổng quan
- ✅ Biểu đồ doanh thu theo ngày
- ✅ Thống kê món bán chạy
- ✅ Bộ lọc thời gian (hôm nay, tuần, tháng)
- ✅ API endpoint `/api/revenue`
- ✅ API endpoint `/api/popular-items`

**Ghi chú:** Chức năng hoạt động tốt, đúng với đặc tả.

---

### ✅ UC-17: Quản lý kho
**Trạng thái:** ✅ **ĐÃ TRIỂN KHAI ĐẦY ĐỦ**

**Đã có:**
- ✅ Xem danh sách tồn kho
- ✅ Nhập kho (tăng tồn kho)
- ✅ Xuất/Hủy kho (giảm tồn kho)
- ✅ API endpoint `/api/inventory-import`
- ✅ API endpoint `/api/inventory-export`
- ✅ API endpoint `/api/inventory`

**Thiếu:**
- ❌ Chưa có chức năng thiết lập định mức tồn kho tối thiểu
- ❌ Chưa có cảnh báo khi tồn kho xuống dưới mức tối thiểu

**Cần thêm:**
- API endpoint để cập nhật minStock (định mức tồn kho tối thiểu)
- Logic cảnh báo khi tồn kho < minStock

---

## TỔNG KẾT

### ✅ Đã triển khai đầy đủ (10/17 Use Cases):
1. UC-02: Đặt món
2. UC-03: Thanh toán đơn hàng
3. UC-05: Gửi phản hồi và đánh giá
4. UC-06: Tạo và quản lý đơn hàng (Tại quầy)
5. UC-07: Cập nhật trạng thái đơn hàng
6. UC-08: Xử lý thanh toán (Tại quầy)
7. UC-09: Chấm công
8. UC-11: Kiểm kê kho
9. UC-16: Xem báo cáo doanh thu, thống kê
10. UC-17: Quản lý kho (thiếu cảnh báo tồn kho)

### ⚠️ Chưa đúng đặc tả (3/17 Use Cases):
1. UC-00: Đăng nhập (dùng Email thay vì Số điện thoại)
2. UC-001: Khôi phục mật khẩu (dùng Email/Token thay vì Số điện thoại/OTP)
3. UC-01: Đăng ký tài khoản (dùng Email thay vì Số điện thoại)

### ⚠️ Chưa có API Backend (4/17 Use Cases):
1. UC-04: Đặt bàn trước
2. UC-12: Báo cáo ca làm
3. UC-13: Quản lý menu
4. UC-14: Tạo chương trình khuyến mãi
5. UC-15: Quản lý nhân viên và khách hàng

### ⚠️ Chưa đầy đủ (1/17 Use Cases):
1. UC-10: Quản lý bàn (thiếu API cập nhật trạng thái)

---

## ĐIỂM SỐ TỔNG THỂ

**Tỷ lệ hoàn thành:** ~59% (10/17 Use Cases đã triển khai đầy đủ)

**Phân loại:**
- ✅ Đầy đủ: 10 Use Cases
- ⚠️ Chưa đúng đặc tả: 3 Use Cases
- ⚠️ Chưa có API Backend: 5 Use Cases
- ⚠️ Chưa đầy đủ: 1 Use Case

---

## KHUYẾN NGHỊ ƯU TIÊN

### Ưu tiên cao:
1. **Sửa UC-00, UC-001, UC-01:** Thay đổi từ Email sang Số điện thoại (ảnh hưởng đến toàn bộ hệ thống)
2. **Thêm API cho UC-04:** Đặt bàn trước (chức năng quan trọng cho khách hàng)
3. **Thêm API cho UC-13:** Quản lý menu (chức năng quan trọng cho quản lý)

### Ưu tiên trung bình:
4. **Thêm API cho UC-12:** Báo cáo ca làm
5. **Thêm API cho UC-14:** Tạo chương trình khuyến mãi
6. **Hoàn thiện UC-10:** Quản lý bàn (thêm API cập nhật trạng thái)
7. **Thêm API cho UC-15:** Quản lý nhân viên và khách hàng

### Ưu tiên thấp:
8. **Hoàn thiện UC-17:** Thêm cảnh báo tồn kho tối thiểu

---

*Báo cáo được tạo vào: 2025-01-XX*

