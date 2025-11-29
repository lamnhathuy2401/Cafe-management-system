# Phân Tích Refactoring Cho Dự Án Coffee Manager

## 📋 Các Loại Refactoring Phổ Biến

### 1. **Extract Method (Trích xuất phương thức)**
Tách một đoạn code dài thành các phương thức nhỏ hơn, dễ đọc và tái sử dụng.

### 2. **Extract Class (Trích xuất lớp)**
Tách một phần logic thành một class riêng để tổ chức code tốt hơn.

### 3. **Extract Variable (Trích xuất biến)**
Thay thế các biểu thức phức tạp bằng biến có tên rõ ràng.

### 4. **Inline Method (Nội tuyến phương thức)**
Loại bỏ phương thức không cần thiết và thay thế bằng code trực tiếp.

### 5. **Rename (Đổi tên)**
Đổi tên biến, hàm, class để code dễ hiểu hơn.

### 6. **Move Method/Field (Di chuyển phương thức/trường)**
Di chuyển method hoặc field đến class phù hợp hơn.

### 7. **Pull Up/Push Down (Kéo lên/Đẩy xuống)**
Di chuyển method/field lên class cha hoặc xuống class con.

### 8. **Replace Magic Number with Named Constant (Thay số ma thuật bằng hằng số)**
Thay các số cứng trong code bằng hằng số có tên.

### 9. **Replace Conditional with Polymorphism (Thay điều kiện bằng đa hình)**
Thay các câu lệnh if/switch bằng đa hình.

### 10. **Replace Parameter with Explicit Methods (Thay tham số bằng phương thức rõ ràng)**
Tách một method có nhiều tham số thành nhiều method riêng.

### 11. **Remove Duplicate Code (Loại bỏ code trùng lặp)**
Xác định và loại bỏ code bị lặp lại.

### 12. **Consolidate Conditional Expression (Gộp biểu thức điều kiện)**
Gộp các điều kiện tương tự thành một.

### 13. **Replace Error Code with Exception (Thay mã lỗi bằng exception)**
Thay việc trả về mã lỗi bằng ném exception.

### 14. **Introduce Parameter Object (Giới thiệu đối tượng tham số)**
Gộp nhiều tham số liên quan thành một object.

### 15. **Preserve Whole Object (Giữ nguyên toàn bộ object)**
Truyền toàn bộ object thay vì nhiều tham số riêng lẻ.

### 16. **Replace Type Code with Class/Enum (Thay mã loại bằng Class/Enum)**
Thay các chuỗi/mã loại bằng class hoặc enum.

### 17. **Replace Nested Conditional with Guard Clauses (Thay điều kiện lồng nhau bằng guard clause)**
Sử dụng early return để giảm độ lồng nhau.

### 18. **Extract Superclass (Trích xuất lớp cha)**
Tạo lớp cha chung cho các class có code tương tự.

### 19. **Replace Inheritance with Delegation (Thay kế thừa bằng ủy quyền)**
Thay kế thừa bằng composition khi phù hợp.

### 20. **Split Large Class (Chia nhỏ class lớn)**
Chia một class quá lớn thành nhiều class nhỏ hơn.

---

## 🔍 Phân Tích Dự Án Coffee Manager

### ❌ **Vấn Đề 1: Code Duplication (Trùng lặp code)**

#### **1.1. Lặp lại kiểm tra xác thực và phân quyền**

**Vị trí:** Nhiều endpoint trong `main.py`

**Ví dụ:**
```python
# Lặp lại ở nhiều nơi:
user = get_current_user(request)
if not user or user["role"] != "manager":
    raise HTTPException(status_code=403)
```

**Số lần xuất hiện:** ~15 lần

**Giải pháp:** Tạo decorator hoặc dependency injection
```python
from functools import wraps
from fastapi import Depends

def require_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user = get_current_user(request)
            if not user or user["role"] not in allowed_roles:
                raise HTTPException(status_code=403)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Sử dụng:
@app.post("/api/menu-items")
@require_role(["manager"])
async def create_menu_item(request: Request):
    # ...
```

#### **1.2. Lặp lại fieldnames cho CSV**

**Vị trí:** `main.py` - 35 lần xuất hiện

**Ví dụ:**
```python
# Lặp lại nhiều lần:
fieldnames = ["id", "name", "category", "price", "image", "description", "status"]
fieldnames = ["id", "number", "capacity", "status"]
fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
```

**Giải pháp:** Tạo constants hoặc class chứa schema
```python
# database.py
class CSVSchemas:
    MENU_ITEMS = ["id", "name", "category", "price", "image", "description", "status"]
    TABLES = ["id", "number", "capacity", "status"]
    ORDERS = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
    # ...
```

#### **1.3. Lặp lại validation logic**

**Vị trí:** Validation giá, ngày tháng, email

**Ví dụ:**
```python
# Lặp lại validation giá:
try:
    price = float(price)
    if price < 0:
        return JSONResponse({
            "success": False,
            "message": "Giá bán phải là số dương"
        }, status_code=400)
except (ValueError, TypeError):
    return JSONResponse({
        "success": False,
        "message": "Giá bán phải là số"
    }, status_code=400)
```

**Giải pháp:** Tạo validation functions
```python
# validators.py
def validate_positive_float(value, field_name="Giá trị"):
    try:
        value = float(value)
        if value < 0:
            raise ValueError(f"{field_name} phải là số dương")
        return value
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} phải là số")
```

---

### ❌ **Vấn Đề 2: Long Method (Phương thức quá dài)**

#### **2.1. Endpoint quá dài**

**Vị trí:** `create_reservation`, `create_promotion`, `submit_shift_report`

**Ví dụ:** `create_reservation` (dòng 463-551) có 88 dòng code

**Giải pháp:** Extract Method
```python
async def create_reservation(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    body = await request.json()
    validate_reservation_data(body)
    
    reservation_datetime = parse_reservation_datetime(body)
    available_table = find_available_table(body, reservation_datetime)
    
    reservation = create_reservation_record(user, body, available_table)
    save_reservation(reservation)
    update_table_status(available_table["id"], "reserved")
    
    return success_response(reservation, available_table)
```

---

### ❌ **Vấn Đề 3: Large Class (Class quá lớn)**

#### **3.1. File main.py quá lớn**

**Vị trí:** `main.py` - 1815 dòng code, tất cả logic trong một file

**Giải pháp:** Split thành modules
```
main.py (chỉ routing)
├── routes/
│   ├── auth.py          # Login, register, password reset
│   ├── menu.py          # Menu items CRUD
│   ├── orders.py        # Order management
│   ├── tables.py        # Table management
│   ├── inventory.py     # Inventory management
│   ├── promotions.py    # Promotions
│   ├── feedback.py      # Feedback
│   ├── staff.py         # Staff management
│   └── reports.py       # Revenue, attendance, etc.
├── services/
│   ├── auth_service.py
│   ├── order_service.py
│   └── validation_service.py
└── models/
    └── schemas.py       # Pydantic models
```

---

### ❌ **Vấn Đề 4: Magic Numbers/Strings (Số/chuỗi ma thuật)**

#### **4.1. Hardcoded strings**

**Vị trí:** Nhiều nơi trong code

**Ví dụ:**
```python
if user["role"] != "manager":  # "manager" là magic string
if table["status"] == "available":  # "available" là magic string
order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"  # "ORD-" là magic string
```

**Giải pháp:** Tạo constants hoặc Enum
```python
# constants.py
class UserRole:
    CUSTOMER = "customer"
    STAFF = "staff"
    MANAGER = "manager"

class TableStatus:
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"

class OrderStatus:
    PENDING = "pending"
    IN_PREPARATION = "in_preparation"
    COMPLETED = "completed"
    WAITING_PAYMENT = "waiting_payment"

class OrderPrefix:
    ORDER = "ORD-"
    RESERVATION = "RES-"
    IMPORT = "IMP-"
    EXPORT = "EXP-"
    TRANSACTION = "TXN-"
```

---

### ❌ **Vấn Đề 5: Duplicate Conditional (Điều kiện trùng lặp)**

#### **5.1. Kiểm tra user role lặp lại**

**Vị trí:** Nhiều endpoint

**Ví dụ:**
```python
if user["role"] == "customer":
    # logic for customer
elif user["role"] == "staff":
    # logic for staff
else:
    # logic for manager
```

**Giải pháp:** Strategy Pattern hoặc Factory Pattern

---

### ❌ **Vấn Đề 6: Long Parameter List (Danh sách tham số dài)**

#### **6.1. Endpoint có nhiều tham số**

**Vị trí:** `create_promotion`, `create_staff`

**Ví dụ:**
```python
async def create_promotion(request: Request):
    body = await request.json()
    name = body.get("name")
    code = body.get("code")
    description = body.get("description", "")
    discount = body.get("discount", 0)
    discount_type = body.get("type", "percentage")
    max_discount = body.get("maxDiscount")
    min_order = body.get("minOrder")
    start_date = body.get("startDate")
    end_date = body.get("endDate")
    # ... 9 tham số
```

**Giải pháp:** Sử dụng Pydantic models
```python
from pydantic import BaseModel, Field
from datetime import date

class PromotionCreate(BaseModel):
    name: str
    code: str
    description: str = ""
    discount: float = Field(ge=0)
    type: str = "percentage"
    maxDiscount: Optional[float] = None
    minOrder: Optional[float] = None
    startDate: date
    endDate: date

@app.post("/api/promotions")
async def create_promotion(promo: PromotionCreate, user: User = Depends(require_manager)):
    # ...
```

---

### ❌ **Vấn Đề 7: Feature Envy (Thèm muốn tính năng)**

#### **7.1. Endpoint xử lý quá nhiều business logic**

**Vị trí:** Nhiều endpoint trong `main.py`

**Ví dụ:** `create_order` xử lý:
- Validation
- Tìm customer
- Cập nhật table status
- Tạo order record
- Tạo order details
- Tính toán total

**Giải pháp:** Tách thành Service Layer
```python
# services/order_service.py
class OrderService:
    def __init__(self, db: Database):
        self.db = db
    
    async def create_order(self, order_data: OrderCreate) -> Order:
        self.validate_order(order_data)
        customer = self.find_customer(order_data.customer_phone)
        table = self.assign_table(order_data.table_id)
        order = self.build_order(order_data, customer, table)
        self.save_order(order)
        return order
```

---

### ❌ **Vấn Đề 8: Data Clumps (Nhóm dữ liệu)**

#### **8.1. Nhóm fieldnames lặp lại**

**Vị trí:** Nhiều nơi sử dụng cùng một nhóm fieldnames

**Giải pháp:** Đã đề cập ở phần 1.2

---

### ❌ **Vấn Đề 9: Primitive Obsession (Ám ảnh kiểu nguyên thủy)**

#### **9.1. Sử dụng string/dict thay vì objects**

**Vị trí:** Toàn bộ dự án sử dụng dict từ CSV

**Ví dụ:**
```python
user = db.find_one("users.csv", "email", email)  # Trả về dict
if user["role"] != "manager":  # Truy cập bằng key string
```

**Giải pháp:** Tạo models/classes
```python
# models/user.py
class User:
    def __init__(self, id: str, name: str, email: str, role: str):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            role=data["role"]
        )
```

---

### ❌ **Vấn Đề 10: Switch Statements (Câu lệnh switch)**

#### **10.1. Nhiều if-elif cho role checking**

**Vị trí:** `get_orders`, `get_reservations`

**Ví dụ:**
```python
if user["role"] == "customer":
    # filter customer orders
elif user["role"] == "staff":
    # show all orders
else:  # manager
    # show all orders with details
```

**Giải pháp:** Strategy Pattern
```python
class OrderFilterStrategy:
    def filter(self, orders, user):
        raise NotImplementedError

class CustomerOrderFilter(OrderFilterStrategy):
    def filter(self, orders, user):
        return [o for o in orders if o.customer_email == user.email]

class StaffOrderFilter(OrderFilterStrategy):
    def filter(self, orders, user):
        return orders

# Factory
def get_order_filter(role: str) -> OrderFilterStrategy:
    strategies = {
        "customer": CustomerOrderFilter(),
        "staff": StaffOrderFilter(),
        "manager": StaffOrderFilter()
    }
    return strategies.get(role, StaffOrderFilter())
```

---

### ❌ **Vấn Đề 11: Comments (Comment không cần thiết)**

#### **11.1. Comment giải thích code rõ ràng**

**Vị trí:** Một số nơi có comment không cần thiết

**Ví dụ:**
```python
# Strip whitespace from email and password
email = email.strip()
password = password.strip()
```

**Giải pháp:** Code tự giải thích, chỉ comment khi cần thiết

---

### ❌ **Vấn Đề 12: Dead Code (Code chết)**

#### **12.1. Function không sử dụng**

**Vị trí:** `get_users_dict()` (dòng 29-32) không được sử dụng

**Giải pháp:** Xóa hoặc sử dụng

---

### ❌ **Vấn Đề 13: Inappropriate Intimacy (Thân mật không phù hợp)**

#### **13.1. Endpoint truy cập trực tiếp database**

**Vị trí:** Tất cả endpoint đều gọi `db.read_csv()`, `db.find_one()` trực tiếp

**Giải pháp:** Sử dụng Repository Pattern
```python
# repositories/user_repository.py
class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def find_by_email(self, email: str) -> Optional[User]:
        data = self.db.find_one("users.csv", "email", email)
        return User.from_dict(data) if data else None
```

---

### ❌ **Vấn Đề 14: Lazy Class (Class lười biếng)**

#### **14.1. Module database.py quá đơn giản**

**Vị trí:** `database.py` chỉ có các hàm utility

**Giải pháp:** Có thể giữ nguyên hoặc mở rộng thành class

---

### ❌ **Vấn Đề 15: Speculative Generality (Tổng quát hóa suy đoán)**

#### **15.1. Có thể không có vấn đề này**

**Vị trí:** Code khá cụ thể, không có abstraction không cần thiết

---

## 📊 Tổng Kết

### Mức Độ Ưu Tiên Refactoring

#### 🔴 **Cao (Cần làm ngay)**
1. **Extract Method** - Tách các endpoint dài
2. **Remove Duplicate Code** - Loại bỏ code trùng lặp (auth check, fieldnames, validation)
3. **Extract Class** - Tách main.py thành modules
4. **Replace Magic String** - Thay bằng constants/enums

#### 🟡 **Trung bình (Nên làm)**
5. **Introduce Parameter Object** - Sử dụng Pydantic models
6. **Extract Service Layer** - Tách business logic
7. **Replace Type Code with Enum** - Sử dụng Enum cho roles, status
8. **Introduce Repository Pattern** - Tách data access

#### 🟢 **Thấp (Có thể làm sau)**
9. **Replace Conditional with Polymorphism** - Strategy pattern
10. **Extract Superclass** - Nếu có nhiều class tương tự
11. **Rename** - Cải thiện tên biến/hàm

---

## 🛠️ Kế Hoạch Refactoring Đề Xuất

### Phase 1: Quick Wins
1. Tạo constants cho magic strings
2. Tạo decorator cho auth check
3. Tạo CSVSchemas class
4. Tạo validation functions

### Phase 2: Restructure 
1. Tách main.py thành routes modules
2. Tạo service layer
3. Sử dụng Pydantic models
4. Tạo repository pattern

### Phase 3: Advanced
1. Implement Strategy pattern cho filtering
2. Tạo models/classes thay vì dict
3. Thêm error handling tốt hơn
4. Thêm logging



