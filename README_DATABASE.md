# Database CSV - Hệ Thống Quản Lý Quán Cà Phê

## Tổng Quan

Hệ thống đã được chuyển đổi từ mock data sang sử dụng database CSV để lưu trữ dữ liệu thực tế.

## Cấu Trúc Database

### Thư Mục `data/`

Tất cả các file CSV được lưu trong thư mục `data/`:

1. **users.csv** - Người dùng (khách hàng, nhân viên, quản lý)
2. **menu_items.csv** - Thực đơn món ăn/đồ uống
3. **orders.csv** - Đơn hàng
4. **order_details.csv** - Chi tiết từng món trong đơn hàng
5. **tables.csv** - Quản lý bàn
6. **inventory.csv** - Nguyên vật liệu kho
7. **promotions.csv** - Chương trình khuyến mãi
8. **feedback.csv** - Phản hồi khách hàng
9. **staff.csv** - Thông tin nhân viên
10. **customers.csv** - Thông tin khách hàng
11. **revenue.csv** - Doanh thu theo ngày
12. **attendance.csv** - Lịch sử chấm công
13. **reservations.csv** - Đặt bàn trước

## Module Database

### `database.py`

Module cung cấp các hàm tiện ích để làm việc với CSV:

- `read_csv(filename)` - Đọc toàn bộ dữ liệu từ CSV
- `write_csv(filename, data, fieldnames)` - Ghi dữ liệu vào CSV
- `append_csv(filename, row, fieldnames)` - Thêm một dòng mới
- `update_csv(filename, key_field, key_value, updates, fieldnames)` - Cập nhật dòng
- `delete_csv(filename, key_field, key_value, fieldnames)` - Xóa dòng
- `find_one(filename, key_field, key_value)` - Tìm một bản ghi
- `find_many(filename, filter_func)` - Tìm nhiều bản ghi với filter

## Các API Đã Được Cập Nhật

### Đọc Dữ Liệu (GET)
- ✅ `/api/menu-items` - Đọc từ `menu_items.csv`
- ✅ `/api/orders` - Đọc từ `orders.csv` và `order_details.csv`
- ✅ `/api/tables` - Đọc từ `tables.csv`
- ✅ `/api/inventory` - Đọc từ `inventory.csv`
- ✅ `/api/promotions` - Đọc từ `promotions.csv`
- ✅ `/api/staff` - Đọc từ `staff.csv`
- ✅ `/api/customers` - Đọc từ `customers.csv`
- ✅ `/api/feedback` - Đọc từ `feedback.csv`
- ✅ `/api/revenue` - Đọc từ `revenue.csv`
- ✅ `/api/popular-items` - Tính toán từ `order_details.csv`
- ✅ `/api/attendance` - Đọc từ `attendance.csv`

### Ghi Dữ Liệu (POST)
- ✅ `/api/register` - Lưu user mới vào `users.csv`
- ✅ `/api/submit-feedback` - Lưu feedback vào `feedback.csv`
- ✅ `/api/process-payment` - Cập nhật `orders.csv`
- ✅ `/api/customer/create-order` - Tạo đơn hàng từ khách hàng
- ✅ `/api/create-order` - Tạo đơn hàng tại quầy
- ✅ `/api/update-order-status` - Cập nhật trạng thái đơn hàng
- ✅ `/api/inventory-check` - Cập nhật `inventory.csv`
- ✅ `/api/inventory-import` - Cập nhật `inventory.csv` (nhập kho)
- ✅ `/api/inventory-export` - Cập nhật `inventory.csv` (xuất/hủy kho)
- ✅ `/api/clock-in-out` - Lưu chấm công vào `attendance.csv`
- ✅ `/api/reset-password` - Cập nhật mật khẩu trong `users.csv`

## Khởi Tạo Database

Các file CSV đã được tạo sẵn với dữ liệu mẫu trong thư mục `data/`.

Nếu cần khởi tạo lại, chạy:
```bash
python init_database.py
```

## Lưu Ý Quan Trọng

1. **Encoding**: Tất cả file CSV sử dụng UTF-8
2. **Kiểu dữ liệu**: Tất cả giá trị trong CSV là string, cần convert khi sử dụng
3. **Tự động tạo thư mục**: Module tự động tạo thư mục `data/` nếu chưa có
4. **Backup**: Nên backup thư mục `data/` định kỳ
5. **Performance**: CSV phù hợp cho dữ liệu nhỏ, với dữ liệu lớn nên chuyển sang SQLite/PostgreSQL

## Cải Thiện So Với Mock Data

- ✅ Dữ liệu được lưu trữ vĩnh viễn
- ✅ Đơn hàng được lưu và có thể xem lại
- ✅ Chấm công được lưu lịch sử
- ✅ Phản hồi được lưu và quản lý
- ✅ Kho được cập nhật thực tế
- ✅ Đăng ký user mới được lưu vào hệ thống

## Tương Lai

Để nâng cấp lên database thực (SQLite/PostgreSQL), chỉ cần:
1. Thay thế các hàm trong `database.py` bằng SQL queries
2. Giữ nguyên interface của các hàm
3. Các API endpoints không cần thay đổi

