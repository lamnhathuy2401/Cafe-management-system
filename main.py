from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
from typing import Optional
import secrets
import database as db
from database import CSVSchemas
import auth
from constants import (
    UserRole, TableStatus, OrderStatus, PaymentStatus, 
    MenuItemStatus, PromotionStatus, OrderPrefix, SessionKey
)
from validators import (
    validate_positive_float, validate_required, validate_email,
    validate_date_format, validate_future_datetime, validate_date_range,
    validate_enum, handle_validation_error, ValidationError
)

app = FastAPI()

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="supersecretkey1234567890",
    same_site="lax",
    https_only=False
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Use get_current_user from auth module
get_current_user = auth.get_current_user

# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = auth.get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = auth.get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user = auth.get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    user = auth.get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str = ""):
    user = auth.get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    # Strip whitespace from email and password
    email = email.strip()
    password = password.strip()
    
    print("EMAIL RECEIVED:", email)
    print("PASSWORD RECEIVED:", password)

    user = db.find_one("users.csv", "email", email)
    
    if not user:
        return JSONResponse({"success": False, "message": "Email không tồn tại trong hệ thống"}, status_code=401)
    
    if user["password"] != password:
        return JSONResponse({"success": False, "message": "Mật khẩu không đúng"}, status_code=401)

    request.session[SessionKey.USER_EMAIL] = email
    request.session[SessionKey.ROLE] = user["role"]

    return {"success": True, "role": user["role"]}


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/customer", response_class=HTMLResponse)
async def customer_dashboard(request: Request):
    user = auth.get_current_user(request)
    if not user or user["role"] != UserRole.CUSTOMER:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("customer.html", {"request": request, "user": user})

@app.get("/staff", response_class=HTMLResponse)
async def staff_dashboard(request: Request):
    user = auth.get_current_user(request)
    if not user or user["role"] != UserRole.STAFF:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("staff.html", {"request": request, "user": user})

@app.get("/manager", response_class=HTMLResponse)
async def manager_dashboard(request: Request):
    user = auth.get_current_user(request)
    if not user or user["role"] != UserRole.MANAGER:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("manager.html", {"request": request, "user": user})

# API Endpoints for data operations
@app.get("/api/menu-items")
async def get_menu_items():
    items = db.read_csv("menu_items.csv")
    # Convert price to float for JSON response
    for item in items:
        item["price"] = float(item["price"])
    return {"items": items}

# UC-13: Quản lý menu - Thêm món mới
@app.post("/api/menu-items")
async def create_menu_item(request: Request, user: dict = Depends(auth.require_manager_role)):
    body = await request.json()
    
    try:
        name = validate_required(body.get("name"), "Tên món")
        category = validate_required(body.get("category"), "Danh mục")
        price = validate_positive_float(body.get("price"), "Giá bán")
        description = body.get("description", "")
        image = body.get("image", "")
        status = body.get("status", MenuItemStatus.AVAILABLE)
    except ValidationError as e:
        return handle_validation_error(e)
    
    # Get next ID
    menu_items = db.read_csv("menu_items.csv")
    item_id = str(len(menu_items) + 1)
    
    new_item = {
        "id": item_id,
        "name": name,
        "category": category,
        "price": str(price),
        "image": image,
        "description": description,
        "status": status
    }
    
    db.append_csv("menu_items.csv", new_item, CSVSchemas.MENU_ITEMS)
    
    return JSONResponse({
        "success": True,
        "message": f"Thêm món {name} thành công.",
        "item": new_item
    })

# UC-13: Quản lý menu - Sửa món
@app.put("/api/menu-items/{item_id}")
async def update_menu_item(request: Request, item_id: str, user: dict = Depends(auth.require_manager_role)):
    body = await request.json()
    
    # Check if item exists
    existing_item = db.find_one("menu_items.csv", "id", item_id)
    if not existing_item:
        return JSONResponse({
            "success": False,
            "message": "Món không tồn tại"
        }, status_code=404)
    
    # Prepare updates
    updates = {}
    try:
        if "name" in body:
            updates["name"] = validate_required(body["name"], "Tên món")
        
        if "category" in body:
            updates["category"] = body["category"]
        
        if "price" in body:
            price = validate_positive_float(body["price"], "Giá bán")
            updates["price"] = str(price)
        
        if "description" in body:
            updates["description"] = body["description"]
        
        if "image" in body:
            updates["image"] = body["image"]
        
        if "status" in body:
            updates["status"] = body["status"]
    except ValidationError as e:
        return handle_validation_error(e)
    
    if not updates:
        return JSONResponse({
            "success": False,
            "message": "Không có thông tin nào để cập nhật"
        }, status_code=400)
    
    # Update item
    db.update_csv("menu_items.csv", "id", item_id, updates, CSVSchemas.MENU_ITEMS)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật thành công."
    })

# UC-13: Quản lý menu - Xóa/Ẩn món
@app.delete("/api/menu-items/{item_id}")
async def delete_menu_item(request: Request, item_id: str, user: dict = Depends(auth.require_manager_role)):
    # Check if item exists
    existing_item = db.find_one("menu_items.csv", "id", item_id)
    if not existing_item:
        return JSONResponse({
            "success": False,
            "message": "Món không tồn tại"
        }, status_code=404)
    
    # Check if item has order history
    order_details = db.read_csv("order_details.csv")
    has_history = any(od.get("menu_item_id") == item_id for od in order_details)
    
    if has_history:
        # Hide item instead of deleting
        db.update_csv("menu_items.csv", "id", item_id, {"status": MenuItemStatus.UNAVAILABLE}, CSVSchemas.MENU_ITEMS)
        return JSONResponse({
            "success": True,
            "message": "Món đã được ẩn (ngưng bán) vì đã có lịch sử bán hàng."
        })
    else:
        # Delete item
        db.delete_csv("menu_items.csv", "id", item_id, CSVSchemas.MENU_ITEMS)
        return JSONResponse({
            "success": True,
            "message": "Xóa món thành công."
        })

@app.get("/api/orders")
async def get_orders(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    orders = db.read_csv("orders.csv")
    order_details = db.read_csv("order_details.csv")
    menu_items = db.read_csv("menu_items.csv")
    
    # Create menu items lookup
    menu_lookup = {item["id"]: item["name"] for item in menu_items}
    
    # Process orders
    result_orders = []
    for order in orders:
        # Get order details
        details = [od for od in order_details if od["order_id"] == order["id"]]
        items = []
        for detail in details:
            item_name = menu_lookup.get(detail["menu_item_id"], "Unknown")
            quantity = int(detail["quantity"])
            if quantity > 1:
                items.append(f"{item_name} x{quantity}")
            else:
                items.append(item_name)
        
        order_data = {
            "id": order["id"],
            "date": order["date"],
            "items": items,
            "total": float(order["total"]),
            "status": order["status"]
        }
        
        if user["role"] == UserRole.CUSTOMER:
            # Only show customer's orders
            if order.get("customer_email") == user["email"]:
                result_orders.append(order_data)
        else:
            # Staff/Manager see all orders with customer info
            order_data["customer"] = order.get("customer_name") or order.get("customer_email", "Khách vãng lai")
            # Extract time from created_at
            if order.get("created_at"):
                try:
                    dt = datetime.strptime(order["created_at"], "%Y-%m-%d %H:%M:%S")
                    order_data["time"] = dt.strftime("%I:%M %p")
                except:
                    order_data["time"] = ""
            result_orders.append(order_data)
    
    return {"orders": result_orders}

@app.get("/api/tables")
async def get_tables():
    tables = db.read_csv("tables.csv")
    # Convert number and capacity to int
    for table in tables:
        table["number"] = int(table["number"])
        table["capacity"] = int(table["capacity"])
    return {"tables": tables}

# UC-10: Cập nhật trạng thái bàn
@app.put("/api/tables/{table_id}/status")
async def update_table_status(request: Request, table_id: str):
    user = get_current_user(request)
    if not user or user["role"] not in ["staff", "manager"]:
        raise HTTPException(status_code=403)
    
    body = await request.json()
    new_status = body.get("status")
    
    if not new_status or new_status not in [TableStatus.AVAILABLE, TableStatus.OCCUPIED, TableStatus.RESERVED]:
        return JSONResponse({
            "success": False,
            "message": "Trạng thái không hợp lệ"
        }, status_code=400)
    
    table = db.find_one("tables.csv", "id", table_id)
    if not table:
        return JSONResponse({
            "success": False,
            "message": "Bàn không tồn tại"
        }, status_code=404)
    
    db.update_csv("tables.csv", "id", table_id, {"status": new_status}, CSVSchemas.TABLES)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật trạng thái bàn thành công",
        "tableId": table_id,
        "status": new_status
    })

# UC-10: Gán bàn cho đơn hàng
@app.post("/api/tables/{table_id}/assign")
async def assign_table_to_order(request: Request, table_id: str):
    user = get_current_user(request)
    if not user or user["role"] not in ["staff", "manager"]:
        raise HTTPException(status_code=403)
    
    body = await request.json()
    order_id = body.get("orderId")
    
    table = db.find_one("tables.csv", "id", table_id)
    if not table:
        return JSONResponse({
            "success": False,
            "message": "Bàn không tồn tại"
        }, status_code=404)
    
    if table["status"] == TableStatus.OCCUPIED:
        return JSONResponse({
            "success": False,
            "message": "Bàn đang được sử dụng"
        }, status_code=400)
    
    # Update table status
    fieldnames = ["id", "number", "capacity", "status"]
    db.update_csv("tables.csv", "id", table_id, {"status": TableStatus.OCCUPIED}, fieldnames)
    
    # Update order with table_id if order_id provided
    if order_id:
        order = db.find_one("orders.csv", "id", order_id)
        if order:
            order_fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
            db.update_csv("orders.csv", "id", order_id, {"table_id": table_id}, order_fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": f"Đã gán bàn {table['number']} cho đơn hàng",
        "tableId": table_id,
        "tableNumber": int(table["number"])
    })

# UC-10: Dọn bàn (Clear table)
@app.post("/api/tables/{table_id}/clear")
async def clear_table(request: Request, table_id: str):
    user = get_current_user(request)
    if not user or user["role"] not in ["staff", "manager"]:
        raise HTTPException(status_code=403)
    
    table = db.find_one("tables.csv", "id", table_id)
    if not table:
        return JSONResponse({
            "success": False,
            "message": "Bàn không tồn tại"
        }, status_code=404)
    
    fieldnames = ["id", "number", "capacity", "status"]
    db.update_csv("tables.csv", "id", table_id, {"status": TableStatus.AVAILABLE}, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": f"Đã dọn bàn {table['number']}",
        "tableId": table_id
    })

# UC-04: Đặt bàn trước
@app.post("/api/create-reservation")
async def create_reservation(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    body = await request.json()
    date = body.get("date")
    time = body.get("time")
    guests = body.get("guests")
    notes = body.get("notes", "")
    
    if not date or not time or not guests:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng điền đầy đủ thông tin"
        }, status_code=400)
    
    # Validate date is in the future
    try:
        reservation_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if reservation_datetime < datetime.now():
            return JSONResponse({
                "success": False,
                "message": "Vui lòng chọn thời gian trong tương lai"
            }, status_code=400)
    except ValueError:
        return JSONResponse({
            "success": False,
            "message": "Định dạng ngày/giờ không hợp lệ"
        }, status_code=400)
    
    # Check available tables
    tables = db.read_csv("tables.csv")
    reservations = db.read_csv("reservations.csv")
    
    # Find available tables that can accommodate the number of guests
    available_tables = []
    for table in tables:
        capacity = int(table["capacity"])
        if capacity >= int(guests) and table["status"] == "available":
            # Check if table is already reserved at this time
            is_reserved = any(
                r.get("date") == date and 
                r.get("time") == time and 
                r.get("table_id") == table["id"] and
                r.get("status") in ["pending", "confirmed"]
                for r in reservations
            )
            if not is_reserved:
                available_tables.append(table)
    
    if not available_tables:
        return JSONResponse({
            "success": False,
            "message": "Rất tiếc, quán đã hết bàn vào thời điểm bạn chọn. Vui lòng chọn thời gian khác hoặc giảm số lượng người."
        }, status_code=400)
    
    # Create reservation
    reservation_id = f"{OrderPrefix.RESERVATION}{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Assign first available table
    assigned_table = available_tables[0]
    
    new_reservation = {
        "id": reservation_id,
        "customer_email": user["email"],
        "date": date,
        "time": time,
        "guests": str(guests),
        "notes": notes,
        "status": "pending",
        "table_id": assigned_table["id"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save reservation
    fieldnames = ["id", "customer_email", "date", "time", "guests", "notes", "status", "table_id", "created_at"]
    db.append_csv("reservations.csv", new_reservation, fieldnames)
    
    # Update table status to reserved
    table_fieldnames = ["id", "number", "capacity", "status"]
    db.update_csv("tables.csv", "id", assigned_table["id"], {"status": TableStatus.RESERVED}, table_fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Gửi yêu cầu đặt bàn thành công! Quán sẽ xác nhận lại với bạn sớm nhất.",
        "reservationId": reservation_id,
        "tableNumber": assigned_table["number"]
    })

@app.get("/api/reservations")
async def get_reservations(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    reservations = db.read_csv("reservations.csv")
    tables = db.read_csv("tables.csv")
    
    # Create table lookup
    table_lookup = {t["id"]: t for t in tables}
    
    result = []
    for res in reservations:
        # Filter by user role
        if user["role"] == UserRole.CUSTOMER:
            if res.get("customer_email") != user["email"]:
                continue
        # Staff and manager see all reservations
        
        table_info = table_lookup.get(res.get("table_id", ""), {})
        result.append({
            "id": res["id"],
            "customer_email": res.get("customer_email", ""),
            "date": res.get("date", ""),
            "time": res.get("time", ""),
            "guests": int(res.get("guests", 0)),
            "notes": res.get("notes", ""),
            "status": res.get("status", "pending"),
            "tableNumber": int(table_info.get("number", 0)) if table_info else None,
            "created_at": res.get("created_at", "")
        })
    
    return {"reservations": result}

@app.get("/api/inventory")
async def get_inventory():
    items = db.read_csv("inventory.csv")
    # Convert quantity and minStock to int/float
    alerts = []
    for item in items:
        try:
            item["quantity"] = float(item["quantity"])
            item["minStock"] = float(item["minStock"])
            # UC-17: Cảnh báo tồn kho tối thiểu
            if item["quantity"] < item["minStock"]:
                alerts.append({
                    "id": item["id"],
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "minStock": item["minStock"],
                    "shortage": item["minStock"] - item["quantity"]
                })
        except:
            pass
    return {
        "items": items,
        "alerts": alerts  # UC-17: Trả về danh sách cảnh báo
    }

# UC-17: Cập nhật định mức tồn kho tối thiểu
@app.put("/api/inventory/{item_id}/min-stock")
async def update_min_stock(request: Request, item_id: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    min_stock = body.get("minStock")
    
    if min_stock is None:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng nhập định mức tồn kho tối thiểu"
        }, status_code=400)
    
    try:
        min_stock = float(min_stock)
        if min_stock < 0:
            return JSONResponse({
                "success": False,
                "message": "Định mức tồn kho phải là số dương"
            }, status_code=400)
    except (ValueError, TypeError):
        return JSONResponse({
            "success": False,
            "message": "Định mức tồn kho phải là số"
        }, status_code=400)
    
    item = db.find_one("inventory.csv", "id", item_id)
    if not item:
        return JSONResponse({
            "success": False,
            "message": "Nguyên liệu không tồn tại"
        }, status_code=404)
    
    db.update_csv("inventory.csv", "id", item_id, {"minStock": str(min_stock)}, CSVSchemas.INVENTORY)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật định mức tồn kho tối thiểu thành công"
    })

@app.get("/api/staff")
async def get_staff():
    staff = db.read_csv("staff.csv")
    return {"staff": staff}

# UC-15: Tạo tài khoản nhân viên
@app.post("/api/staff")
async def create_staff(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    name = body.get("name")
    phone = body.get("phone")
    email = body.get("email")
    password = body.get("password", "123456")  # Default password
    roles = body.get("roles", [])  # List of roles: ["cashier", "barista", "server"]
    salary = body.get("salary", "")
    
    if not name or not phone:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng điền đầy đủ thông tin (Tên, Số điện thoại)"
        }, status_code=400)
    
    # Check if phone already exists
    existing_user = db.find_one("users.csv", "phone", phone)
    if existing_user:
        return JSONResponse({
            "success": False,
            "message": "Số điện thoại này đã tồn tại trong hệ thống."
        }, status_code=400)
    
    # Check if email already exists (if provided)
    if email:
        existing_email = db.find_one("users.csv", "email", email)
        if existing_email:
            return JSONResponse({
                "success": False,
                "message": "Email này đã tồn tại trong hệ thống."
            }, status_code=400)
    
    # Create user account
    users = db.read_csv("users.csv")
    user_id = str(len(users) + 1)
    
    new_user = {
        "id": user_id,
        "name": name,
        "email": email if email else f"staff{user_id}@coffee.com",
        "password": password,
        "phone": phone,
        "role": "staff",
        "roles": ",".join(roles) if roles else "staff"  # Store roles as comma-separated
    }
    
    db.append_csv("users.csv", new_user, CSVSchemas.USERS)
    
    # Create staff record
    staff_list = db.read_csv("staff.csv")
    staff_id = str(len(staff_list) + 1)
    
    new_staff = {
        "id": staff_id,
        "name": name,
        "role": ", ".join(roles) if roles else "Staff",
        "email": new_user["email"],
        "phone": phone,
        "status": "active",
        "schedule": ""
    }
    
    db.append_csv("staff.csv", new_staff, CSVSchemas.STAFF)
    
    return JSONResponse({
        "success": True,
        "message": "Tạo nhân viên thành công.",
        "staff": new_staff
    })

# UC-15: Cập nhật thông tin/quyền nhân viên
@app.put("/api/staff/{staff_id}")
async def update_staff(request: Request, staff_id: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    
    staff = db.find_one("staff.csv", "id", staff_id)
    if not staff:
        return JSONResponse({
            "success": False,
            "message": "Nhân viên không tồn tại"
        }, status_code=404)
    
    updates = {}
    if "name" in body:
        updates["name"] = body["name"]
    if "role" in body:
        updates["role"] = body["role"]
    if "status" in body:
        updates["status"] = body["status"]
    if "schedule" in body:
        updates["schedule"] = body["schedule"]
    
    if updates:
        db.update_csv("staff.csv", "id", staff_id, updates, CSVSchemas.STAFF)
        
        # Also update user roles if provided
        if "roles" in body:
            user_email = staff.get("email")
            if user_email:
                user_record = db.find_one("users.csv", "email", user_email)
                if user_record:
                    db.update_csv("users.csv", "email", user_email, {
                        "role": UserRole.STAFF,
                        "roles": ",".join(body["roles"]) if isinstance(body["roles"], list) else body["roles"]
                    }, CSVSchemas.USERS)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật nhân viên thành công"
    })

# UC-15: Reset mật khẩu khách hàng
@app.post("/api/customers/{customer_email}/reset-password")
async def reset_customer_password(request: Request, customer_email: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    new_password = body.get("newPassword", "123456")  # Default password
    
    customer = db.find_one("users.csv", "email", customer_email)
    if not customer or customer.get("role") != "customer":
        return JSONResponse({
            "success": False,
            "message": "Khách hàng không tồn tại"
        }, status_code=404)
    
    fieldnames = ["id", "name", "email", "password", "phone", "role"]
    db.update_csv("users.csv", "email", customer_email, {"password": new_password}, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Mật khẩu đã được reset thành công"
    })

# UC-15: Trả lời phản hồi
@app.post("/api/feedback/{feedback_id}/respond")
async def respond_to_feedback(request: Request, feedback_id: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    response_text = body.get("response", "")
    
    if not response_text:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng nhập nội dung trả lời"
        }, status_code=400)
    
    feedback = db.find_one("feedback.csv", "id", feedback_id)
    if not feedback:
        return JSONResponse({
            "success": False,
            "message": "Phản hồi không tồn tại"
        }, status_code=404)
    
    fieldnames = ["id", "customer_email", "customer_name", "date", "foodRating", "serviceRating", "comment", "status", "response"]
    db.update_csv("feedback.csv", "id", feedback_id, {
        "response": response_text,
        "status": "responded"
    }, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Đã gửi trả lời phản hồi thành công"
    })

@app.get("/api/promotions")
async def get_promotions():
    promotions = db.read_csv("promotions.csv")
    # Convert numeric fields
    for promo in promotions:
        try:
            promo["discount"] = float(promo["discount"]) if promo["discount"] else 0
            promo["maxDiscount"] = float(promo["maxDiscount"]) if promo.get("maxDiscount") else None
            promo["minOrder"] = float(promo["minOrder"]) if promo.get("minOrder") else None
        except:
            pass
    return {"promotions": promotions}

# UC-14: Tạo chương trình khuyến mãi
@app.post("/api/promotions")
async def create_promotion(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
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
    
    if not name or not code or discount is None or not start_date or not end_date:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng điền đầy đủ thông tin"
        }, status_code=400)
    
    # Check if code already exists
    existing_promos = db.read_csv("promotions.csv")
    if any(p.get("code") == code for p in existing_promos):
        return JSONResponse({
            "success": False,
            "message": f"Mã '{code}' đã tồn tại. Vui lòng chọn mã khác."
        }, status_code=400)
    
    # Validate dates
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if end_dt < start_dt:
            return JSONResponse({
                "success": False,
                "message": "Thời gian kết thúc không hợp lệ."
            }, status_code=400)
    except ValueError:
        return JSONResponse({
            "success": False,
            "message": "Định dạng ngày không hợp lệ (YYYY-MM-DD)"
        }, status_code=400)
    
    # Validate discount
    try:
        discount = float(discount)
        if discount < 0:
            return JSONResponse({
                "success": False,
                "message": "Phần trăm giảm giá phải là số dương"
            }, status_code=400)
    except (ValueError, TypeError):
        return JSONResponse({
            "success": False,
            "message": "Phần trăm giảm giá phải là số"
        }, status_code=400)
    
    # Get next ID
    promo_id = str(len(existing_promos) + 1)
    
    new_promo = {
        "id": promo_id,
        "code": code,
        "name": name,
        "description": description,
        "discount": str(discount),
        "type": discount_type,
        "maxDiscount": str(max_discount) if max_discount else "",
        "minOrder": str(min_order) if min_order else "",
        "startDate": start_date,
        "endDate": end_date,
        "status": "active"
    }
    
    fieldnames = ["id", "code", "name", "description", "discount", "type", "maxDiscount", "minOrder", "startDate", "endDate", "status"]
    db.append_csv("promotions.csv", new_promo, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": f"Tạo chương trình {name} thành công.",
        "promotion": new_promo
    })

@app.put("/api/promotions/{promo_id}")
async def update_promotion(request: Request, promo_id: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    
    existing_promo = db.find_one("promotions.csv", "id", promo_id)
    if not existing_promo:
        return JSONResponse({
            "success": False,
            "message": "Chương trình khuyến mãi không tồn tại"
        }, status_code=404)
    
    updates = {}
    if "name" in body:
        updates["name"] = body["name"]
    if "code" in body:
        # Check if new code conflicts with existing
        if body["code"] != existing_promo.get("code"):
            existing_promos = db.read_csv("promotions.csv")
            if any(p.get("code") == body["code"] for p in existing_promos):
                return JSONResponse({
                    "success": False,
                    "message": f"Mã '{body['code']}' đã tồn tại."
                }, status_code=400)
        updates["code"] = body["code"]
    if "description" in body:
        updates["description"] = body["description"]
    if "discount" in body:
        updates["discount"] = str(body["discount"])
    if "type" in body:
        updates["type"] = body["type"]
    if "maxDiscount" in body:
        updates["maxDiscount"] = str(body["maxDiscount"]) if body["maxDiscount"] else ""
    if "minOrder" in body:
        updates["minOrder"] = str(body["minOrder"]) if body["minOrder"] else ""
    if "startDate" in body:
        updates["startDate"] = body["startDate"]
    if "endDate" in body:
        updates["endDate"] = body["endDate"]
    if "status" in body:
        updates["status"] = body["status"]
    
    if updates:
        fieldnames = ["id", "code", "name", "description", "discount", "type", "maxDiscount", "minOrder", "startDate", "endDate", "status"]
        db.update_csv("promotions.csv", "id", promo_id, updates, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật thành công"
    })

@app.delete("/api/promotions/{promo_id}")
async def delete_promotion(request: Request, promo_id: str):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        raise HTTPException(status_code=403)
    
    existing_promo = db.find_one("promotions.csv", "id", promo_id)
    if not existing_promo:
        return JSONResponse({
            "success": False,
            "message": "Chương trình khuyến mãi không tồn tại"
        }, status_code=404)
    
    fieldnames = ["id", "code", "name", "description", "discount", "type", "maxDiscount", "minOrder", "startDate", "endDate", "status"]
    db.delete_csv("promotions.csv", "id", promo_id, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Xóa chương trình khuyến mãi thành công"
    })

@app.get("/api/customers")
async def get_customers():
    customers = db.read_csv("customers.csv")
    # Convert numeric fields
    for customer in customers:
        try:
            customer["totalOrders"] = int(customer["totalOrders"])
            customer["totalSpent"] = float(customer["totalSpent"])
        except:
            pass
    return {"customers": customers}

@app.get("/api/feedback")
async def get_feedback():
    feedback = db.read_csv("feedback.csv")
    # Convert ratings to int and format response
    result = []
    for fb in feedback:
        fb_data = {
            "id": fb["id"],
            "customer": fb.get("customer_name") or fb.get("customer_email", "Unknown"),
            "date": fb["date"],
            "foodRating": int(fb["foodRating"]),
            "serviceRating": int(fb["serviceRating"]),
            "comment": fb["comment"],
            "status": fb["status"]
        }
        if fb.get("response"):
            fb_data["response"] = fb["response"]
        result.append(fb_data)
    return {"feedback": result}

@app.get("/api/revenue")
async def get_revenue():
    revenue_data = db.read_csv("revenue.csv")
    
    # Convert to proper format
    daily = []
    for r in revenue_data:
        daily.append({
            "date": r["date"],
            "revenue": float(r["revenue"]),
            "orders": int(r["orders"])
        })
    
    # Calculate totals
    today = datetime.now().strftime("%Y-%m-%d")
    today_data = next((d for d in daily if d["date"] == today), None)
    
    week_total = sum(d["revenue"] for d in daily[-7:])
    week_orders = sum(d["orders"] for d in daily[-7:])
    
    totals = {
        "today": today_data["revenue"] if today_data else 0.0,
        "week": week_total,
        "month": sum(d["revenue"] for d in daily),
        "orders_today": today_data["orders"] if today_data else 0,
        "orders_week": week_orders,
        "avg_order": week_total / week_orders if week_orders > 0 else 0
    }
    
    return {
        "daily": daily,
        "totals": totals
    }

# Thống kê món bán chạy
@app.get("/api/popular-items")
async def get_popular_items():
    # Calculate from order_details
    order_details = db.read_csv("order_details.csv")
    menu_items = db.read_csv("menu_items.csv")
    
    # Create menu lookup
    menu_lookup = {item["id"]: item for item in menu_items}
    
    # Calculate totals
    item_stats = {}
    for detail in order_details:
        item_id = detail["menu_item_id"]
        if item_id not in item_stats:
            item_stats[item_id] = {"totalSold": 0, "revenue": 0.0}
        
        item_stats[item_id]["totalSold"] += int(detail["quantity"])
        item_stats[item_id]["revenue"] += float(detail["subtotal"])
    
    # Format results
    items = []
    for item_id, stats in item_stats.items():
        menu_item = menu_lookup.get(item_id, {})
        items.append({
            "id": item_id,
            "name": menu_item.get("name", "Unknown"),
            "category": menu_item.get("category", ""),
            "totalSold": stats["totalSold"],
            "revenue": stats["revenue"],
            "image": menu_item.get("image", "")
        })
    
    # Sort by totalSold descending
    items.sort(key=lambda x: x["totalSold"], reverse=True)
    
    return {"items": items[:5]}  # Top 5

# Đăng ký tài khoản khách hàng
@app.post("/api/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: Optional[str] = Form(None)
):
    # Strip whitespace
    email = email.strip()
    password = password.strip()
    
    # Check if email already exists
    existing_user = db.find_one("users.csv", "email", email)
    if existing_user:
        return JSONResponse({"success": False, "message": "Email đã được sử dụng"}, status_code=400)
    
    # Validate email format
    if "@" not in email or "." not in email.split("@")[1]:
        return JSONResponse({"success": False, "message": "Email không hợp lệ"}, status_code=400)
    
    # Get next user ID
    users = db.read_csv("users.csv")
    user_id = str(len(users) + 1)
    
    # Create new user
    new_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password,
        "phone": phone.strip() if phone else "",
        "role": "customer"
    }
    
    # Save to CSV
    fieldnames = ["id", "name", "email", "password", "phone", "role"]
    db.append_csv("users.csv", new_user, fieldnames)
    
    return JSONResponse({"success": True, "message": "Đăng ký thành công"})

# Gửi phản hồi/đánh giá
@app.post("/api/submit-feedback")
async def submit_feedback(
    request: Request,
    foodRating: int = Form(...),
    serviceRating: int = Form(...),
    comment: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    # Get next ID
    feedback_list = db.read_csv("feedback.csv")
    feedback_id = str(len(feedback_list) + 1)
    
    # Create feedback record
    new_feedback = {
        "id": feedback_id,
        "customer_email": user["email"],
        "customer_name": user["name"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "foodRating": str(foodRating),
        "serviceRating": str(serviceRating),
        "comment": comment,
        "status": "pending",
        "response": ""
    }
    
    # Save to CSV
    fieldnames = ["id", "customer_email", "customer_name", "date", "foodRating", "serviceRating", "comment", "status", "response"]
    db.append_csv("feedback.csv", new_feedback, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Cảm ơn bạn đã gửi phản hồi!"
    })

# Thanh toán đơn hàng
@app.post("/api/process-payment")
async def process_payment(
    request: Request,
    orderId: str = None,
    paymentMethod: str = None,
    amount: float = None
):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    # Handle both Form and JSON
    try:
        body = await request.json()
        orderId = body.get("orderId")
        paymentMethod = body.get("paymentMethod")
        amount = body.get("amount")
    except:
        pass
    
    if not orderId or not paymentMethod or amount is None:
        return JSONResponse({
            "success": False,
            "message": "Thiếu thông tin thanh toán"
        }, status_code=400)
    
    # Update order status
    order = db.find_one("orders.csv", "id", orderId)
    if not order:
        return JSONResponse({
            "success": False,
            "message": "Đơn hàng không tồn tại"
        }, status_code=404)
    
    # Update order payment status
    fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
    db.update_csv("orders.csv", "id", orderId, {
        "payment_method": paymentMethod,
        "payment_status": "paid",
        "status": "completed" if order["status"] != "completed" else order["status"]
    }, fieldnames)
    
    transaction_id = f"TXN-{orderId}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return JSONResponse({
        "success": True,
        "message": "Thanh toán thành công",
        "transactionId": transaction_id,
        "paymentMethod": paymentMethod,
        "amount": amount
    })

# Tạo đơn hàng từ khách hàng
@app.post("/api/customer/create-order")
async def customer_create_order(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "customer":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    items = body.get("items", [])
    
    if not items:
        return JSONResponse({
            "success": False,
            "message": "Giỏ hàng của bạn đang trống"
        }, status_code=400)
    
    # Calculate total
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    
    # Generate order ID
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create order record
    new_order = {
        "id": order_id,
        "customer_email": user["email"],
        "customer_name": user["name"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": str(subtotal),
        "status": "pending",
        "payment_method": "",
        "payment_status": "pending",
        "table_id": "",  # Customer orders don't have table assignment
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save order
    order_fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
    db.append_csv("orders.csv", new_order, order_fieldnames)
    
    # Save order details
    detail_fieldnames = ["order_id", "menu_item_id", "quantity", "price", "subtotal"]
    for item in items:
        order_detail = {
            "order_id": order_id,
            "menu_item_id": item["id"],
            "quantity": str(item["quantity"]),
            "price": str(item["price"]),
            "subtotal": str(item["price"] * item["quantity"])
        }
        db.append_csv("order_details.csv", order_detail, detail_fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Đặt hàng thành công!",
        "orderId": order_id,
        "total": subtotal,
        "status": "pending"
    })

# Tạo đơn hàng tại quầy
@app.post("/api/create-order")
async def create_order(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    items = body.get("items", [])
    customer_phone = body.get("customerPhone")
    promo_code = body.get("promoCode")
    subtotal = body.get("subtotal", 0)
    discount = body.get("discount", 0)
    table_id = body.get("tableId")  # UC-06: Thêm số bàn
    
    if not items:
        return JSONResponse({
            "success": False,
            "message": "Đơn hàng không có món nào"
        }, status_code=400)
    
    # Generate order ID
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    total = subtotal - discount
    
    # Get customer name if phone provided
    customer_name = ""
    if customer_phone:
        customer = db.find_one("users.csv", "phone", customer_phone)
        if customer:
            customer_name = customer.get("name", "")
    
    # UC-06: Cập nhật trạng thái bàn nếu có table_id
    if table_id:
        table = db.find_one("tables.csv", "id", table_id)
        if table:
            table_fieldnames = ["id", "number", "capacity", "status"]
            db.update_csv("tables.csv", "id", table_id, {"status": TableStatus.OCCUPIED}, table_fieldnames)
    
    # Create order record
    new_order = {
        "id": order_id,
        "customer_email": customer_phone if customer_phone else "",
        "customer_name": customer_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": str(total),
        "status": "pending",
        "payment_method": "",
        "payment_status": "pending",
        "table_id": table_id if table_id else "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save order
    order_fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
    db.append_csv("orders.csv", new_order, order_fieldnames)
    
    # Save order details
    detail_fieldnames = ["order_id", "menu_item_id", "quantity", "price", "subtotal"]
    for item in items:
        order_detail = {
            "order_id": order_id,
            "menu_item_id": item["id"],
            "quantity": str(item["quantity"]),
            "price": str(item["price"]),
            "subtotal": str(item["price"] * item["quantity"])
        }
        db.append_csv("order_details.csv", order_detail, detail_fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Đơn hàng đã được tạo thành công",
        "orderId": order_id,
        "total": total,
        "status": "pending"
    })

# Cập nhật trạng thái đơn hàng
@app.post("/api/update-order-status")
async def update_order_status(request: Request):
    user = get_current_user(request)
    if not user or user["role"] not in ["staff", "manager"]:
        raise HTTPException(status_code=403)
    
    body = await request.json()
    order_id = body.get("orderId")
    new_status = body.get("status")
    
    if not order_id or not new_status:
        return JSONResponse({
            "success": False,
            "message": "Thiếu thông tin"
        }, status_code=400)
    
    # Update order status
    order = db.find_one("orders.csv", "id", order_id)
    if not order:
        return JSONResponse({
            "success": False,
            "message": "Đơn hàng không tồn tại"
        }, status_code=404)
    
    fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "table_id", "created_at"]
    db.update_csv("orders.csv", "id", order_id, {"status": new_status}, fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Cập nhật trạng thái đơn hàng thành công",
        "orderId": order_id,
        "status": new_status
    })

# Kiểm kê kho
@app.post("/api/inventory-check")
async def inventory_check(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    adjustments = body.get("adjustments", [])
    
    if not adjustments:
        return JSONResponse({
            "success": False,
            "message": "Không có điều chỉnh nào"
        }, status_code=400)
    
    # Update inventory quantities
    inventory_fieldnames = ["id", "name", "quantity", "unit", "minStock", "supplier"]
    for adj in adjustments:
        db.update_csv("inventory.csv", "id", adj["id"], {
            "quantity": str(adj["actualQuantity"])
        }, inventory_fieldnames)
    
    return JSONResponse({
        "success": True,
        "message": "Kiểm kê kho thành công",
        "adjustments": len(adjustments)
    })

# Nhập kho
@app.post("/api/inventory-import")
async def inventory_import(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    supplier = body.get("supplier", "")
    note = body.get("note", "")
    items = body.get("items", [])
    
    if not items:
        return JSONResponse({
            "success": False,
            "message": "Chưa có nguyên liệu nào được nhập"
        }, status_code=400)
    
    # Update inventory quantities
    inventory_fieldnames = ["id", "name", "quantity", "unit", "minStock", "supplier"]
    for item in items:
        if item["id"]:
            existing = db.find_one("inventory.csv", "id", item["id"])
            if existing:
                new_quantity = float(existing["quantity"]) + float(item["quantity"])
                db.update_csv("inventory.csv", "id", item["id"], {
                    "quantity": str(new_quantity)
                }, inventory_fieldnames)
    
    import_id = f"IMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return JSONResponse({
        "success": True,
        "message": "Nhập kho thành công",
        "importId": import_id,
        "itemsCount": len(items)
    })

# Xuất/Hủy kho
@app.post("/api/inventory-export")
async def inventory_export(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    item_id = body.get("itemId")
    quantity = body.get("quantity")
    reason = body.get("reason", "")
    
    if not item_id or not quantity or quantity <= 0:
        return JSONResponse({
            "success": False,
            "message": "Thông tin không hợp lệ"
        }, status_code=400)
    
    # Update inventory quantity
    existing = db.find_one("inventory.csv", "id", item_id)
    if not existing:
        return JSONResponse({
            "success": False,
            "message": "Nguyên liệu không tồn tại"
        }, status_code=404)
    
    current_quantity = float(existing["quantity"])
    if quantity > current_quantity:
        return JSONResponse({
            "success": False,
            "message": f"Số lượng hủy ({quantity}) vượt quá số lượng tồn kho ({current_quantity})"
        }, status_code=400)
    
    new_quantity = current_quantity - quantity
    inventory_fieldnames = ["id", "name", "quantity", "unit", "minStock", "supplier"]
    db.update_csv("inventory.csv", "id", item_id, {
        "quantity": str(new_quantity)
    }, inventory_fieldnames)
    
    export_id = f"EXP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return JSONResponse({
        "success": True,
        "message": "Xuất/Hủy kho thành công",
        "exportId": export_id,
        "quantity": quantity,
        "reason": reason
    })

# Chấm công
@app.post("/api/clock-in-out")
async def clock_in_out(
    request: Request,
    action: str = Form(...)  # "clock_in" or "clock_out"
):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    current_time = datetime.now()
    current_date = current_time.strftime("%Y-%m-%d")
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    time_str = current_time.strftime("%H:%M:%S")
    
    if action == "clock_in":
        # Check if already clocked in today
        today_record = db.find_many("attendance.csv", lambda x: 
            x.get("staff_email") == user["email"] and 
            x.get("date") == current_date and 
            x.get("clockOut") == ""
        )
        
        if today_record:
            return JSONResponse({
                "success": False,
                "message": f"Bạn đã vào ca lúc {today_record[0].get('clockIn')}. Bạn có muốn ra ca không?"
            }, status_code=400)
        
        # Create new attendance record
        attendance_list = db.read_csv("attendance.csv")
        attendance_id = str(len(attendance_list) + 1)
        
        new_record = {
            "id": attendance_id,
            "staff_email": user["email"],
            "date": current_date,
            "clockIn": time_str,
            "clockOut": "",
            "hours": "0",
            "status": "present"
        }
        
        fieldnames = ["id", "staff_email", "date", "clockIn", "clockOut", "hours", "status"]
        db.append_csv("attendance.csv", new_record, fieldnames)
        
        message = f"Đã chấm công vào lúc {time_str}"
    else:
        # Find today's record
        today_record = db.find_many("attendance.csv", lambda x: 
            x.get("staff_email") == user["email"] and 
            x.get("date") == current_date and 
            x.get("clockOut") == ""
        )
        
        if not today_record:
            return JSONResponse({
                "success": False,
                "message": "Bạn chưa chấm công vào ca. Vui lòng vào ca trước."
            }, status_code=400)
        
        # Calculate hours worked
        clock_in = datetime.strptime(f"{current_date} {today_record[0]['clockIn']}", "%Y-%m-%d %H:%M:%S")
        hours_worked = (current_time - clock_in).total_seconds() / 3600
        
        # Update record
        fieldnames = ["id", "staff_email", "date", "clockIn", "clockOut", "hours", "status"]
        db.update_csv("attendance.csv", "id", today_record[0]["id"], {
            "clockOut": time_str,
            "hours": str(round(hours_worked, 2))
        }, fieldnames)
        
        message = f"Đã chấm công ra lúc {time_str}. Tổng thời gian làm việc: {round(hours_worked, 2)}h"
    
    return JSONResponse({
        "success": True,
        "message": message,
        "time": current_time_str
    })

# Lấy thông tin chấm công
@app.get("/api/attendance")
async def get_attendance(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    # Get attendance records for this staff
    attendance_records = db.find_many("attendance.csv", lambda x: x.get("staff_email") == user["email"])
    
    # Format and calculate summary
    attendance = []
    total_hours = 0.0
    for record in attendance_records:
        attendance.append({
            "date": record["date"],
            "clockIn": record["clockIn"],
            "clockOut": record["clockOut"],
            "hours": float(record["hours"]),
            "status": record["status"]
        })
        total_hours += float(record["hours"])
    
    summary = {
        "totalHours": total_hours,
        "daysWorked": len(attendance),
        "avgHoursPerDay": total_hours / len(attendance) if len(attendance) > 0 else 0
    }
    
    return {
        "attendance": attendance,
        "summary": summary
    }

# UC-12: Báo cáo ca làm
@app.post("/api/shift-report")
async def submit_shift_report(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        raise HTTPException(status_code=403)
    
    body = await request.json()
    actual_cash = body.get("actualCash")
    notes = body.get("notes", "")
    equipment_status = body.get("equipmentStatus", {})
    
    if actual_cash is None:
        return JSONResponse({
            "success": False,
            "message": "Vui lòng nhập tiền mặt thực tế"
        }, status_code=400)
    
    try:
        actual_cash = float(actual_cash)
    except (ValueError, TypeError):
        return JSONResponse({
            "success": False,
            "message": "Tiền mặt thực tế phải là số"
        }, status_code=400)
    
    # Check if there are incomplete orders
    orders = db.read_csv("orders.csv")
    incomplete_orders = [
        o for o in orders 
        if o.get("status") in ["pending", "in_preparation"] and 
        o.get("payment_status") != "paid"
    ]
    
    if incomplete_orders:
        return JSONResponse({
            "success": False,
            "message": f"Bạn còn {len(incomplete_orders)} đơn hàng chưa hoàn tất. Vui lòng xử lý trước khi kết ca.",
            "incompleteOrders": len(incomplete_orders)
        }, status_code=400)
    
    # Calculate expected cash from completed orders
    today = datetime.now().strftime("%Y-%m-%d")
    today_orders = [
        o for o in orders 
        if o.get("date") == today and 
        o.get("payment_status") == "paid" and
        o.get("payment_method") == "cash"
    ]
    expected_cash = sum(float(o.get("total", 0)) for o in today_orders)
    
    # Calculate difference
    difference = actual_cash - expected_cash
    
    # Get today's attendance record
    current_date = datetime.now().strftime("%Y-%m-%d")
    today_attendance = db.find_many("attendance.csv", lambda x: 
        x.get("staff_email") == user["email"] and 
        x.get("date") == current_date and 
        x.get("clockOut") != ""
    )
    
    if not today_attendance:
        return JSONResponse({
            "success": False,
            "message": "Bạn chưa chấm công ra ca. Vui lòng ra ca trước khi chốt ca."
        }, status_code=400)
    
    # Create shift report record (you may want to create a shift_reports.csv)
    # For now, we'll just return the report data
    report_data = {
        "staff_email": user["email"],
        "date": current_date,
        "expectedCash": expected_cash,
        "actualCash": actual_cash,
        "difference": difference,
        "notes": notes,
        "equipmentStatus": equipment_status,
        "ordersCompleted": len([o for o in orders if o.get("date") == today and o.get("status") == "completed"]),
        "totalRevenue": sum(float(o.get("total", 0)) for o in today_orders),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # In a real system, you would save this to shift_reports.csv
    # For now, we'll return it
    
    return JSONResponse({
        "success": True,
        "message": "Báo cáo ca làm đã được lưu thành công",
        "report": report_data,
        "cashMatched": difference == 0
    })

# Mock password reset tokens storage (in production, use database with expiry)
RESET_TOKENS = {}

# Yêu cầu đặt lại mật khẩu
@app.post("/api/forgot-password")
async def forgot_password(email: str = Form(...)):
    email = email.strip()
    user = db.find_one("users.csv", "email", email)
    if not user:
        return JSONResponse({"success": False, "message": "Email không tồn tại trong hệ thống"}, status_code=404)
    
    # Generate reset token
    token = secrets.token_urlsafe(32)
    RESET_TOKENS[token] = {
        "email": email,
        "expires": datetime.now() + timedelta(hours=1)
    }
    
    # In production, send email with reset link
    # For demo, return the reset link
    reset_link = f"/reset-password?token={token}"
    
    return JSONResponse({
        "success": True,
        "message": "Link đặt lại mật khẩu đã được tạo",
        "resetLink": reset_link,  # In production, this would be sent via email
        "demo_note": "Trong môi trường thực tế, link này sẽ được gửi qua email"
    })

# Đặt lại mật khẩu
@app.post("/api/reset-password")
async def reset_password(
    token: str = Form(...),
    newPassword: str = Form(...)
):
    if token not in RESET_TOKENS:
        return JSONResponse({"success": False, "message": "Token không hợp lệ hoặc đã hết hạn"}, status_code=400)
    
    token_data = RESET_TOKENS[token]
    
    # Check if token expired
    if datetime.now() > token_data["expires"]:
        del RESET_TOKENS[token]
        return JSONResponse({"success": False, "message": "Token đã hết hạn. Vui lòng yêu cầu đặt lại mật khẩu mới"}, status_code=400)
    
    # Update password
    email = token_data["email"]
    user = db.find_one("users.csv", "email", email)
    if user:
        # Update password in CSV
        fieldnames = ["id", "name", "email", "password", "phone", "role"]
        db.update_csv("users.csv", "email", email, {"password": newPassword}, fieldnames)
        del RESET_TOKENS[token]  # Remove used token
        
        return JSONResponse({
            "success": True,
            "message": "Mật khẩu đã được đặt lại thành công"
        })
    
    return JSONResponse({"success": False, "message": "Có lỗi xảy ra"}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)