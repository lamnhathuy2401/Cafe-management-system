# Hướng Dẫn Thiết Lập Database CSV

## Cấu trúc Database

Hệ thống sử dụng các file CSV để lưu trữ dữ liệu trong thư mục `data/`:

### Các file CSV:

1. **users.csv** - Thông tin người dùng (khách hàng, nhân viên, quản lý)
2. **menu_items.csv** - Danh sách món ăn/đồ uống
3. **orders.csv** - Đơn hàng
4. **order_details.csv** - Chi tiết từng món trong đơn hàng
5. **tables.csv** - Thông tin bàn
6. **inventory.csv** - Nguyên vật liệu trong kho
7. **promotions.csv** - Chương trình khuyến mãi
8. **feedback.csv** - Phản hồi và đánh giá từ khách hàng
9. **staff.csv** - Thông tin nhân viên (bổ sung)
10. **customers.csv** - Thông tin khách hàng (bổ sung)
11. **revenue.csv** - Dữ liệu doanh thu theo ngày
12. **attendance.csv** - Lịch sử chấm công
13. **reservations.csv** - Đặt bàn trước

## Khởi tạo Database

Để tạo các file CSV với dữ liệu mẫu, chạy lệnh:

```bash
python init_database.py
```

Lệnh này sẽ:
- Tạo thư mục `data/` nếu chưa có
- Tạo tất cả các file CSV với dữ liệu mẫu
- Hiển thị thông báo xác nhận cho từng file

## Module Database

File `database.py` cung cấp các hàm tiện ích:

- `read_csv(filename)` - Đọc dữ liệu từ CSV
- `write_csv(filename, data, fieldnames)` - Ghi dữ liệu vào CSV
- `append_csv(filename, row, fieldnames)` - Thêm một dòng mới
- `update_csv(filename, key_field, key_value, updates, fieldnames)` - Cập nhật dòng
- `delete_csv(filename, key_field, key_value, fieldnames)` - Xóa dòng
- `find_one(filename, key_field, key_value)` - Tìm một bản ghi
- `find_many(filename, filter_func)` - Tìm nhiều bản ghi với filter

## Lưu ý

- Tất cả dữ liệu được lưu dưới dạng string trong CSV
- Cần convert sang số khi sử dụng (int, float)
- Encoding: UTF-8
- Tự động tạo thư mục `data/` nếu chưa tồn tại

