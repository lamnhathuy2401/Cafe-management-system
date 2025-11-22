# Hệ Thống Quản Lý Quán Cà Phê

Hệ thống quản lý quán cà phê toàn diện được xây dựng bằng **FastAPI**, **HTML**, **Tailwind CSS**, và **JavaScript/jQuery**. Hệ thống hỗ trợ 3 vai trò: Khách hàng, Nhân viên và Quản lý với các chức năng quản lý đầy đủ.

## 📋 Mục Lục

- [Tính Năng Chính](#tính-năng-chính)
- [Công Nghệ Sử Dụng](#công-nghệ-sử-dụng)
- [Cài Đặt và Chạy Ứng Dụng](#cài-đặt-và-chạy-ứng-dụng)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [API Endpoints](#api-endpoints)
- [Tài Khoản Demo](#tài-khoản-demo)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [Cấu Trúc Database](#cấu-trúc-database)
- [Tùy Biến và Mở Rộng](#tùy-biến-và-mở-rộng)

## ✨ Tính Năng Chính

### 🎯 1. Dashboard Khách Hàng

- **Xem thực đơn**: Duyệt menu với hình ảnh, danh mục và giá cả
- **Giỏ hàng**: Thêm/xóa món, điều chỉnh số lượng
- **Đặt hàng**: Đặt hàng trực tuyến với xác nhận tức thì
- **Đặt bàn trước**: Đặt bàn với ngày, giờ và số lượng khách
- **Lịch sử đơn hàng**: Xem các đơn hàng đã đặt với trạng thái
- **Phản hồi**: Đánh giá và nhận xét về chất lượng món ăn và dịch vụ
- **Áp dụng khuyến mãi**: Nhập mã khuyến mãi để giảm giá

### 👨‍💼 2. Dashboard Nhân Viên

- **Quản lý đơn hàng**: Xử lý đơn hàng qua quy trình (chờ xử lý → đang làm → hoàn thành)
- **Quản lý bàn**: Cập nhật trạng thái bàn (trống, đang dùng, đã đặt)
- **Tạo đơn tại quầy**: Tạo đơn hàng trực tiếp tại quầy với chọn bàn
- **Thanh toán**: Xử lý thanh toán cho đơn hàng (tiền mặt, thẻ, ví điện tử)
- **Kiểm kê kho**: Cập nhật số lượng tồn kho trong ca làm việc
- **Nhập/Xuất kho**: Quản lý nhập kho và xuất/hủy kho
- **Báo cáo ca**: Gửi báo cáo cuối ca với ghi chú và tình trạng thiết bị
- **Chấm công**: Theo dõi giờ vào/ra ca và tổng giờ làm việc
- **Nhật ký hoạt động**: Theo dõi tất cả hoạt động trong ca

### 👔 3. Dashboard Quản Lý

- **Phân tích doanh thu**:
  - Theo dõi doanh thu theo ngày, tuần, tháng
  - Biểu đồ tương tác hiển thị xu hướng
  - Tính toán giá trị đơn hàng trung bình
  - Xem các món bán chạy nhất
- **Quản lý thực đơn**: Thao tác CRUD đầy đủ cho món ăn (thêm, sửa, xóa)
- **Quản lý nhân viên**: Xem và quản lý thông tin nhân viên
- **Quản lý khách hàng**:
  - Xem hồ sơ khách hàng
  - Theo dõi chi tiêu và lịch sử đơn hàng
  - Tìm kiếm khách hàng
- **Quản lý phản hồi**:
  - Xem tất cả phản hồi khách hàng
  - Lọc theo trạng thái và đánh giá
  - Trả lời phản hồi trực tiếp
- **Quản lý kho hàng**:
  - Theo dõi mức tồn kho
  - Cảnh báo tồn kho thấp
  - Thông tin nhà cung cấp
  - Thêm/sửa/xóa nguyên liệu
- **Quản lý khuyến mãi**: Tạo và quản lý các chương trình khuyến mãi

## 🛠️ Công Nghệ Sử Dụng

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, Tailwind CSS, jQuery, JavaScript
- **Biểu đồ**: Chart.js
- **Icons**: Font Awesome
- **Quản lý phiên**: Starlette Session Middleware
- **Lưu trữ dữ liệu**: CSV files (có thể nâng cấp lên database)

## 📦 Cài Đặt và Chạy Ứng Dụng

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (Python package manager)

### Các Bước Cài Đặt

1. **Clone hoặc tải dự án về máy**

2. **Cài đặt các thư viện Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Khởi tạo database (tùy chọn)**:
   ```bash
   python init_database.py
   ```
   Lệnh này sẽ tạo các file CSV với dữ liệu mẫu trong thư mục `data/`.

4. **Chạy ứng dụng**:
   ```bash
   # Cách 1: Chạy trực tiếp
   python main.py
   
   # Cách 2: Sử dụng uvicorn (khuyến nghị)
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Truy cập ứng dụng**:
   Mở trình duyệt và truy cập:
   ```
   http://localhost:8000
   ```

## 📁 Cấu Trúc Dự Án

```
coffee manager/
├── main.py                      # Ứng dụng FastAPI và các API endpoints
├── database.py                  # Module xử lý CSV database
├── init_database.py             # Script khởi tạo database với dữ liệu mẫu
├── requirements.txt             # Các thư viện Python cần thiết
├── README.md                    # File này
├── README_DATABASE.md           # Tài liệu về database CSV
├── DATABASE_SETUP.md            # Hướng dẫn thiết lập database
├── BAO_CAO_KIEM_TRA_DAC_TA.md  # Báo cáo kiểm tra đặc tả
│
├── data/                        # Thư mục chứa các file CSV
│   ├── users.csv                # Người dùng (khách hàng, nhân viên, quản lý)
│   ├── menu_items.csv           # Món ăn/đồ uống
│   ├── orders.csv               # Đơn hàng
│   ├── order_details.csv        # Chi tiết từng món trong đơn hàng
│   ├── tables.csv               # Thông tin bàn
│   ├── inventory.csv            # Nguyên vật liệu trong kho
│   ├── promotions.csv           # Chương trình khuyến mãi
│   ├── feedback.csv             # Phản hồi khách hàng
│   ├── staff.csv                # Thông tin nhân viên
│   ├── customers.csv            # Thông tin khách hàng
│   ├── revenue.csv              # Dữ liệu doanh thu
│   ├── attendance.csv            # Lịch sử chấm công
│   └── reservations.csv         # Đặt bàn trước
│
├── templates/                    # Các template HTML
│   ├── base.html                # Template cơ sở với styles chung
│   ├── login.html               # Trang đăng nhập
│   ├── register.html            # Trang đăng ký
│   ├── forgot_password.html     # Trang quên mật khẩu
│   ├── reset_password.html      # Trang đặt lại mật khẩu
│   ├── customer.html            # Dashboard khách hàng
│   ├── staff.html               # Dashboard nhân viên
│   └── manager.html             # Dashboard quản lý
│
├── static/                       # Thư mục chứa file tĩnh (CSS, JS, images)
└── styles/                      # Thư mục chứa file CSS
    └── globals.css               # CSS toàn cục
```

## 🔌 API Endpoints

### Xác Thực

- `GET /` - Trang chủ (redirect đến dashboard theo vai trò)
- `GET /login` - Trang đăng nhập
- `POST /login` - Xác thực đăng nhập
- `GET /register` - Trang đăng ký
- `POST /api/register` - Đăng ký tài khoản mới
- `GET /forgot-password` - Trang quên mật khẩu
- `POST /api/forgot-password` - Gửi yêu cầu đặt lại mật khẩu
- `GET /reset-password` - Trang đặt lại mật khẩu
- `POST /api/reset-password` - Đặt lại mật khẩu
- `GET /logout` - Đăng xuất

### Dashboards

- `GET /customer` - Dashboard khách hàng
- `GET /staff` - Dashboard nhân viên
- `GET /manager` - Dashboard quản lý

### API Dữ Liệu

#### Menu
- `GET /api/menu-items` - Lấy danh sách món ăn
- `POST /api/menu-items` - Thêm món mới (quản lý)
- `PUT /api/menu-items/{item_id}` - Cập nhật món (quản lý)
- `DELETE /api/menu-items/{item_id}` - Xóa món (quản lý)

#### Đơn Hàng
- `GET /api/orders` - Lấy danh sách đơn hàng (theo vai trò)
- `POST /api/create-order` - Tạo đơn hàng tại quầy (nhân viên)
- `POST /api/customer/create-order` - Tạo đơn hàng từ khách hàng
- `PUT /api/orders/{order_id}/status` - Cập nhật trạng thái đơn hàng

#### Bàn
- `GET /api/tables` - Lấy danh sách bàn
- `PUT /api/tables/{table_id}/status` - Cập nhật trạng thái bàn
- `POST /api/tables/{table_id}/assign` - Gán bàn cho đơn hàng
- `POST /api/tables/{table_id}/clear` - Dọn dẹp bàn

#### Đặt Bàn
- `GET /api/reservations` - Lấy danh sách đặt bàn
- `POST /api/create-reservation` - Tạo đặt bàn mới

#### Kho Hàng
- `GET /api/inventory` - Lấy danh sách nguyên liệu
- `POST /api/inventory-check` - Kiểm kê kho
- `POST /api/inventory-import` - Nhập kho
- `POST /api/inventory-export` - Xuất/hủy kho
- `PUT /api/inventory/{item_id}/min-stock` - Cập nhật mức tồn kho tối thiểu

#### Khuyến Mãi
- `GET /api/promotions` - Lấy danh sách khuyến mãi
- `POST /api/promotions` - Tạo khuyến mãi mới (quản lý)
- `PUT /api/promotions/{promo_id}` - Cập nhật khuyến mãi (quản lý)
- `DELETE /api/promotions/{promo_id}` - Xóa khuyến mãi (quản lý)

#### Phản Hồi
- `GET /api/feedback` - Lấy danh sách phản hồi
- `POST /api/submit-feedback` - Gửi phản hồi (khách hàng)
- `POST /api/feedback/{feedback_id}/respond` - Trả lời phản hồi (quản lý)

#### Nhân Viên
- `GET /api/staff` - Lấy danh sách nhân viên
- `POST /api/staff` - Tạo nhân viên mới (quản lý)
- `PUT /api/staff/{staff_id}` - Cập nhật thông tin nhân viên (quản lý)

#### Khách Hàng
- `GET /api/customers` - Lấy danh sách khách hàng
- `POST /api/customers/{customer_email}/reset-password` - Đặt lại mật khẩu khách hàng (quản lý)

#### Doanh Thu
- `GET /api/revenue` - Lấy dữ liệu doanh thu
- `GET /api/popular-items` - Lấy danh sách món bán chạy

#### Chấm Công
- `GET /api/attendance` - Lấy lịch sử chấm công
- `POST /api/clock-in-out` - Chấm công vào/ra ca

#### Báo Cáo Ca
- `POST /api/shift-report` - Gửi báo cáo ca làm việc

#### Thanh Toán
- `POST /api/process-payment` - Xử lý thanh toán

## 👤 Tài Khoản Demo

### Tài Khoản Khách Hàng
- **Email**: `customer@demo.com`
- **Mật khẩu**: `customer123`

### Tài Khoản Nhân Viên
- **Email**: `staff@demo.com`
- **Mật khẩu**: `staff123`

### Tài Khoản Quản Lý
- **Email**: `manager@demo.com`
- **Mật khẩu**: `manager123`

> **Lưu ý**: Các tài khoản demo này được tạo tự động khi chạy `init_database.py`. Bạn có thể đăng ký tài khoản mới thông qua trang đăng ký.

## 📖 Hướng Dẫn Sử Dụng

### Cho Khách Hàng

1. **Đăng nhập/Đăng ký**: Truy cập trang đăng nhập và đăng nhập hoặc đăng ký tài khoản mới
2. **Xem menu**: Duyệt các món ăn và đồ uống có sẵn
3. **Thêm vào giỏ hàng**: Click vào món để thêm vào giỏ hàng, điều chỉnh số lượng
4. **Áp dụng khuyến mãi**: Nhập mã khuyến mãi (nếu có) để được giảm giá
5. **Đặt hàng**: Xác nhận đơn hàng và chờ xử lý
6. **Đặt bàn**: Chọn ngày, giờ và số lượng khách để đặt bàn trước
7. **Xem lịch sử**: Xem các đơn hàng đã đặt và trạng thái của chúng
8. **Gửi phản hồi**: Đánh giá và nhận xét về dịch vụ

### Cho Nhân Viên

1. **Đăng nhập**: Đăng nhập bằng tài khoản nhân viên
2. **Tạo đơn tại quầy**: 
   - Chọn tab "Tạo Đơn"
   - Chọn món từ menu
   - Chọn bàn (nếu có)
   - Tạo đơn hàng
3. **Quản lý đơn hàng**: 
   - Xem danh sách đơn hàng
   - Cập nhật trạng thái (Bắt đầu → Hoàn thành)
4. **Quản lý bàn**: 
   - Xem trạng thái các bàn
   - Cập nhật trạng thái bàn (trống/đang dùng/đã đặt)
5. **Thanh toán**: Xử lý thanh toán cho các đơn hàng đã hoàn thành
6. **Kiểm kê kho**: Kiểm tra và cập nhật số lượng tồn kho
7. **Nhập/Xuất kho**: Quản lý nhập kho và xuất/hủy kho
8. **Báo cáo ca**: Gửi báo cáo cuối ca với ghi chú
9. **Chấm công**: Chấm công vào/ra ca và xem lịch sử

### Cho Quản Lý

1. **Đăng nhập**: Đăng nhập bằng tài khoản quản lý
2. **Xem báo cáo**: 
   - Xem doanh thu theo ngày/tuần/tháng
   - Xem biểu đồ xu hướng
   - Xem các món bán chạy nhất
3. **Quản lý menu**: 
   - Thêm món mới
   - Sửa thông tin món
   - Xóa/ẩn món
4. **Quản lý nhân viên**: Xem và quản lý thông tin nhân viên
5. **Quản lý khách hàng**: 
   - Xem danh sách khách hàng
   - Tìm kiếm khách hàng
   - Xem chi tiết đơn hàng và chi tiêu
6. **Quản lý phản hồi**: 
   - Xem tất cả phản hồi
   - Lọc theo trạng thái
   - Trả lời phản hồi
7. **Quản lý kho**: 
   - Xem tồn kho
   - Thêm/sửa/xóa nguyên liệu
   - Xem cảnh báo tồn kho thấp
8. **Quản lý khuyến mãi**: 
   - Tạo chương trình khuyến mãi mới
   - Sửa/xóa khuyến mãi

## 💾 Cấu Trúc Database

Hệ thống sử dụng các file CSV để lưu trữ dữ liệu trong thư mục `data/`. Mỗi file CSV đại diện cho một bảng dữ liệu:

- **users.csv**: Thông tin người dùng (email, password, role, name, phone)
- **menu_items.csv**: Món ăn/đồ uống (id, name, category, price, description, image, status)
- **orders.csv**: Đơn hàng (id, customer_id, staff_id, total, status, created_at, table_id)
- **order_details.csv**: Chi tiết đơn hàng (id, order_id, item_id, quantity, price)
- **tables.csv**: Thông tin bàn (id, number, capacity, status)
- **inventory.csv**: Nguyên liệu (id, name, quantity, unit, supplier, minStock)
- **promotions.csv**: Khuyến mãi (id, name, code, type, discount, startDate, endDate, status)
- **feedback.csv**: Phản hồi (id, customer_id, foodRating, serviceRating, comment, response, status, date)
- **staff.csv**: Nhân viên (id, name, email, phone, role, status, schedule)
- **customers.csv**: Khách hàng (id, name, email, phone, totalOrders, totalSpent, status)
- **revenue.csv**: Doanh thu (id, date, amount)
- **attendance.csv**: Chấm công (id, staff_id, date, clockIn, clockOut, totalHours)
- **reservations.csv**: Đặt bàn (id, customer_id, table_id, date, time, guests, status)

Xem thêm chi tiết trong `README_DATABASE.md` và `DATABASE_SETUP.md`.

## 🔧 Tùy Biến và Mở Rộng

### Thêm Database Thật

Để thêm database thật (PostgreSQL, MySQL, SQLite):

1. Cài đặt driver database (ví dụ: `pip install databases asyncpg` cho PostgreSQL)
2. Cập nhật `main.py` để sử dụng database thay vì CSV
3. Tạo models và migrations
4. Cập nhật `database.py` để sử dụng ORM hoặc raw SQL

### Tùy Chỉnh Giao Diện

- **Tailwind CSS**: Được load từ CDN, có thể tùy chỉnh trong `templates/base.html`
- **Custom CSS**: Thêm styles trong `styles/globals.css`
- **Icons**: Sử dụng Font Awesome, có thể thay đổi icon trong các template HTML

### Thêm Tính Năng Mới

1. **Thêm route mới**: Thêm endpoint trong `main.py`
2. **Tạo template mới**: Tạo file HTML trong `templates/`
3. **Thêm JavaScript**: Thêm logic JavaScript trong các template hoặc file riêng trong `static/`
4. **Cập nhật database**: Thêm file CSV mới hoặc cột mới trong file CSV hiện có

### Cải Thiện Bảo Mật

- Thay đổi `secret_key` trong SessionMiddleware
- Thêm xác thực JWT thay vì session
- Thêm rate limiting
- Thêm CORS middleware nếu cần
- Mã hóa mật khẩu (hiện tại lưu plain text)

## ⚠️ Lưu Ý

- Đây là ứng dụng demo với dữ liệu lưu trong CSV files
- Xác thực dựa trên session (chưa sẵn sàng cho production)
- Không có xử lý thanh toán thật
- Không có thông báo email
- Không có cập nhật real-time (cần refresh trang)
- Mật khẩu được lưu dạng plain text (nên mã hóa trong production)

## 🚀 Cải Tiến Tương Lai

Các tính năng có thể thêm vào:

- ✅ Tích hợp database thật (PostgreSQL/MySQL)
- ✅ WebSocket cho cập nhật real-time
- ✅ Tích hợp cổng thanh toán
- ✅ Thông báo email
- ✅ Đăng ký người dùng (đã có)
- ✅ Upload file cho hình ảnh món ăn
- ✅ Báo cáo và phân tích nâng cao
- ✅ Ứng dụng mobile
- ✅ Đặt hàng bằng QR code
- ✅ Chương trình khách hàng thân thiết
- ✅ Mã hóa mật khẩu
- ✅ Xác thực 2 yếu tố
- ✅ Quản lý quyền chi tiết hơn

## 📄 Giấy Phép

Đây là dự án demo cho mục đích giáo dục.

## 📞 Hỗ Trợ

Nếu có vấn đề hoặc câu hỏi, vui lòng tham khảo tài liệu hoặc liên hệ nhóm phát triển.

---

**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: 2024
