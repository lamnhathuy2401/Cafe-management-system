"""
Script to initialize CSV database with sample data
"""
import os
import csv
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def init_users():
    """Initialize users.csv"""
    users = [
        {
            "id": "1",
            "name": "Demo Customer",
            "email": "customer@demo.com",
            "password": "customer123",
            "phone": "0901234567",
            "role": "customer"
        },
        {
            "id": "2",
            "name": "Demo Staff",
            "email": "staff@demo.com",
            "password": "staff123",
            "phone": "0901234568",
            "role": "staff"
        },
        {
            "id": "3",
            "name": "Demo Manager",
            "email": "manager@demo.com",
            "password": "manager123",
            "phone": "0901234569",
            "role": "manager"
        }
    ]
    
    fieldnames = ["id", "name", "email", "password", "phone", "role"]
    filepath = os.path.join(DATA_DIR, "users.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)
    
    print(f"✓ Created {filepath} with {len(users)} users")

def init_menu_items():
    """Initialize menu_items.csv"""
    menu_items = [
        {"id": "1", "name": "Espresso", "category": "Hot Coffee", "price": "3.50", "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6df5bee?w=400", "description": "Cà phê espresso đậm đà", "status": "available"},
        {"id": "2", "name": "Cappuccino", "category": "Hot Coffee", "price": "4.50", "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400", "description": "Cappuccino với bọt sữa", "status": "available"},
        {"id": "3", "name": "Latte", "category": "Hot Coffee", "price": "4.75", "image": "https://images.unsplash.com/photo-1561882468-9110e03e0f78?w=400", "description": "Latte mềm mịn", "status": "available"},
        {"id": "4", "name": "Americano", "category": "Hot Coffee", "price": "3.75", "image": "https://images.unsplash.com/photo-1532004491497-ba35c367d634?w=400", "description": "Americano đậm đà", "status": "available"},
        {"id": "5", "name": "Iced Coffee", "category": "Cold Coffee", "price": "4.25", "image": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=400", "description": "Cà phê đá mát lạnh", "status": "available"},
        {"id": "6", "name": "Cold Brew", "category": "Cold Coffee", "price": "4.50", "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400", "description": "Cold brew mát lạnh", "status": "available"},
        {"id": "7", "name": "Croissant", "category": "Pastries", "price": "3.25", "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400", "description": "Bánh sừng bò giòn tan", "status": "available"},
        {"id": "8", "name": "Blueberry Muffin", "category": "Pastries", "price": "3.50", "image": "https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=400", "description": "Muffin việt quất thơm ngon", "status": "available"},
    ]
    
    fieldnames = ["id", "name", "category", "price", "image", "description", "status"]
    filepath = os.path.join(DATA_DIR, "menu_items.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(menu_items)
    
    print(f"✓ Created {filepath} with {len(menu_items)} menu items")

def init_orders():
    """Initialize orders.csv"""
    orders = [
        {
            "id": "ORD-001",
            "customer_email": "customer@demo.com",
            "date": "2025-11-15",
            "total": "7.75",
            "status": "completed",
            "payment_method": "cash",
            "payment_status": "paid",
            "created_at": "2025-11-15 10:30:00"
        },
        {
            "id": "ORD-002",
            "customer_email": "customer@demo.com",
            "date": "2025-11-18",
            "total": "4.75",
            "status": "waiting_payment",
            "payment_method": "",
            "payment_status": "pending",
            "created_at": "2025-11-18 14:20:00"
        },
        {
            "id": "ORD-003",
            "customer_email": "customer@demo.com",
            "date": "2025-11-19",
            "total": "6.75",
            "status": "pending",
            "payment_method": "",
            "payment_status": "pending",
            "created_at": "2025-11-19 09:15:00"
        },
        {
            "id": "ORD-101",
            "customer_email": "",
            "customer_name": "John Doe",
            "date": "2025-11-19",
            "total": "7.00",
            "status": "pending",
            "payment_method": "",
            "payment_status": "pending",
            "created_at": "2025-11-19 10:30:00"
        },
        {
            "id": "ORD-102",
            "customer_email": "",
            "customer_name": "Jane Smith",
            "date": "2025-11-19",
            "total": "8.25",
            "status": "waiting_payment",
            "payment_method": "",
            "payment_status": "pending",
            "created_at": "2025-11-19 10:45:00"
        },
        {
            "id": "ORD-103",
            "customer_email": "",
            "customer_name": "Bob Johnson",
            "date": "2025-11-19",
            "total": "4.50",
            "status": "completed",
            "payment_method": "cash",
            "payment_status": "paid",
            "created_at": "2025-11-19 11:00:00"
        }
    ]
    
    fieldnames = ["id", "customer_email", "customer_name", "date", "total", "status", "payment_method", "payment_status", "created_at"]
    filepath = os.path.join(DATA_DIR, "orders.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
    
    print(f"✓ Created {filepath} with {len(orders)} orders")

def init_order_details():
    """Initialize order_details.csv"""
    order_details = [
        {"order_id": "ORD-001", "menu_item_id": "2", "quantity": "1", "price": "4.50", "subtotal": "4.50"},
        {"order_id": "ORD-001", "menu_item_id": "7", "quantity": "1", "price": "3.25", "subtotal": "3.25"},
        {"order_id": "ORD-002", "menu_item_id": "3", "quantity": "1", "price": "4.75", "subtotal": "4.75"},
        {"order_id": "ORD-003", "menu_item_id": "1", "quantity": "1", "price": "3.50", "subtotal": "3.50"},
        {"order_id": "ORD-003", "menu_item_id": "7", "quantity": "1", "price": "3.25", "subtotal": "3.25"},
        {"order_id": "ORD-101", "menu_item_id": "1", "quantity": "2", "price": "3.50", "subtotal": "7.00"},
        {"order_id": "ORD-102", "menu_item_id": "3", "quantity": "1", "price": "4.75", "subtotal": "4.75"},
        {"order_id": "ORD-102", "menu_item_id": "8", "quantity": "1", "price": "3.50", "subtotal": "3.50"},
        {"order_id": "ORD-103", "menu_item_id": "6", "quantity": "1", "price": "4.50", "subtotal": "4.50"},
    ]
    
    fieldnames = ["order_id", "menu_item_id", "quantity", "price", "subtotal"]
    filepath = os.path.join(DATA_DIR, "order_details.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(order_details)
    
    print(f"✓ Created {filepath} with {len(order_details)} order details")

def init_tables():
    """Initialize tables.csv"""
    tables = [
        {"id": "1", "number": "1", "capacity": "2", "status": "available"},
        {"id": "2", "number": "2", "capacity": "4", "status": "occupied"},
        {"id": "3", "number": "3", "capacity": "4", "status": "available"},
        {"id": "4", "number": "4", "capacity": "6", "status": "reserved"},
        {"id": "5", "number": "5", "capacity": "2", "status": "available"},
        {"id": "6", "number": "6", "capacity": "8", "status": "available"},
    ]
    
    fieldnames = ["id", "number", "capacity", "status"]
    filepath = os.path.join(DATA_DIR, "tables.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tables)
    
    print(f"✓ Created {filepath} with {len(tables)} tables")

def init_inventory():
    """Initialize inventory.csv"""
    inventory = [
        {"id": "1", "name": "Coffee Beans (Arabica)", "quantity": "45", "unit": "kg", "minStock": "20", "supplier": "Premium Beans Co."},
        {"id": "2", "name": "Milk", "quantity": "15", "unit": "liters", "minStock": "30", "supplier": "Local Dairy Farm"},
        {"id": "3", "name": "Sugar", "quantity": "25", "unit": "kg", "minStock": "10", "supplier": "Sweet Supply Inc."},
        {"id": "4", "name": "Paper Cups (12oz)", "quantity": "500", "unit": "pieces", "minStock": "200", "supplier": "Packaging Pro"},
        {"id": "5", "name": "Croissants", "quantity": "8", "unit": "pieces", "minStock": "20", "supplier": "Baker's Delight"},
    ]
    
    fieldnames = ["id", "name", "quantity", "unit", "minStock", "supplier"]
    filepath = os.path.join(DATA_DIR, "inventory.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)
    
    print(f"✓ Created {filepath} with {len(inventory)} inventory items")

def init_promotions():
    """Initialize promotions.csv"""
    promotions = [
        {
            "id": "1",
            "code": "HAPPY20",
            "name": "Happy Hour",
            "description": "20% off all drinks",
            "discount": "20",
            "type": "percentage",
            "maxDiscount": "50000",
            "minOrder": "100000",
            "startDate": "2025-11-01",
            "endDate": "2025-11-30",
            "status": "active"
        },
        {
            "id": "2",
            "code": "WEEKEND",
            "name": "Weekend Special",
            "description": "Buy 2 Get 1 Free",
            "discount": "0",
            "type": "bogo",
            "maxDiscount": "",
            "minOrder": "",
            "startDate": "2025-11-15",
            "endDate": "2025-12-15",
            "status": "active"
        },
        {
            "id": "3",
            "code": "XMAS20",
            "name": "Giáng Sinh An Lành",
            "description": "Giảm 20%",
            "discount": "20",
            "type": "percentage",
            "maxDiscount": "50000",
            "minOrder": "100000",
            "startDate": "2025-12-01",
            "endDate": "2025-12-31",
            "status": "active"
        }
    ]
    
    fieldnames = ["id", "code", "name", "description", "discount", "type", "maxDiscount", "minOrder", "startDate", "endDate", "status"]
    filepath = os.path.join(DATA_DIR, "promotions.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(promotions)
    
    print(f"✓ Created {filepath} with {len(promotions)} promotions")

def init_feedback():
    """Initialize feedback.csv"""
    feedback = [
        {
            "id": "1",
            "customer_email": "customer@demo.com",
            "customer_name": "John Doe",
            "date": "2025-11-08",
            "foodRating": "5",
            "serviceRating": "5",
            "comment": "Excellent coffee and very friendly staff!",
            "status": "pending",
            "response": ""
        },
        {
            "id": "2",
            "customer_email": "customer@demo.com",
            "customer_name": "Jane Smith",
            "date": "2025-11-07",
            "foodRating": "5",
            "serviceRating": "5",
            "comment": "Best coffee shop in town!",
            "status": "responded",
            "response": "Thank you for your support!"
        },
        {
            "id": "3",
            "customer_email": "customer@demo.com",
            "customer_name": "Bob Johnson",
            "date": "2025-11-06",
            "foodRating": "3",
            "serviceRating": "4",
            "comment": "Good service, but my latte was a bit cold.",
            "status": "pending",
            "response": ""
        }
    ]
    
    fieldnames = ["id", "customer_email", "customer_name", "date", "foodRating", "serviceRating", "comment", "status", "response"]
    filepath = os.path.join(DATA_DIR, "feedback.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(feedback)
    
    print(f"✓ Created {filepath} with {len(feedback)} feedback entries")

def init_staff():
    """Initialize staff.csv"""
    staff = [
        {
            "id": "1",
            "name": "Sarah Johnson",
            "role": "Barista",
            "email": "sarah@coffee.com",
            "phone": "(555) 123-4567",
            "status": "active",
            "schedule": "Mon-Fri, 6AM-2PM"
        },
        {
            "id": "2",
            "name": "Mike Chen",
            "role": "Cashier",
            "email": "mike@coffee.com",
            "phone": "(555) 234-5678",
            "status": "active",
            "schedule": "Tue-Sat, 10AM-6PM"
        },
        {
            "id": "3",
            "name": "Emily Rodriguez",
            "role": "Barista",
            "email": "emily@coffee.com",
            "phone": "(555) 345-6789",
            "status": "active",
            "schedule": "Wed-Sun, 7AM-3PM"
        }
    ]
    
    fieldnames = ["id", "name", "role", "email", "phone", "status", "schedule"]
    filepath = os.path.join(DATA_DIR, "staff.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(staff)
    
    print(f"✓ Created {filepath} with {len(staff)} staff members")

def init_customers():
    """Initialize customers.csv"""
    customers = [
        {
            "id": "1",
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "(555) 111-2222",
            "totalOrders": "24",
            "totalSpent": "387.50",
            "status": "active"
        },
        {
            "id": "2",
            "name": "Jane Smith",
            "email": "jane.smith@email.com",
            "phone": "(555) 222-3333",
            "totalOrders": "18",
            "totalSpent": "295.75",
            "status": "active"
        },
        {
            "id": "3",
            "name": "Bob Johnson",
            "email": "bob.j@email.com",
            "phone": "(555) 333-4444",
            "totalOrders": "32",
            "totalSpent": "512.25",
            "status": "active"
        }
    ]
    
    fieldnames = ["id", "name", "email", "phone", "totalOrders", "totalSpent", "status"]
    filepath = os.path.join(DATA_DIR, "customers.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customers)
    
    print(f"✓ Created {filepath} with {len(customers)} customers")

def init_revenue():
    """Initialize revenue.csv"""
    revenue = [
        {"date": "2025-11-13", "revenue": "1245.50", "orders": "87"},
        {"date": "2025-11-14", "revenue": "1398.25", "orders": "92"},
        {"date": "2025-11-15", "revenue": "1156.75", "orders": "78"},
        {"date": "2025-11-16", "revenue": "1520.00", "orders": "105"},
        {"date": "2025-11-17", "revenue": "1687.50", "orders": "115"},
        {"date": "2025-11-18", "revenue": "1823.25", "orders": "128"},
        {"date": "2025-11-19", "revenue": "945.00", "orders": "62"},
    ]
    
    fieldnames = ["date", "revenue", "orders"]
    filepath = os.path.join(DATA_DIR, "revenue.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(revenue)
    
    print(f"✓ Created {filepath} with {len(revenue)} revenue records")

def init_attendance():
    """Initialize attendance.csv"""
    attendance = [
        {"id": "1", "staff_email": "staff@demo.com", "date": "2025-11-19", "clockIn": "08:00:00", "clockOut": "16:30:00", "hours": "8.5", "status": "present"},
        {"id": "2", "staff_email": "staff@demo.com", "date": "2025-11-18", "clockIn": "08:05:00", "clockOut": "16:25:00", "hours": "8.33", "status": "present"},
        {"id": "3", "staff_email": "staff@demo.com", "date": "2025-11-17", "clockIn": "08:10:00", "clockOut": "16:35:00", "hours": "8.42", "status": "present"},
        {"id": "4", "staff_email": "staff@demo.com", "date": "2025-11-16", "clockIn": "08:00:00", "clockOut": "16:00:00", "hours": "8.0", "status": "present"},
        {"id": "5", "staff_email": "staff@demo.com", "date": "2025-11-15", "clockIn": "08:15:00", "clockOut": "16:30:00", "hours": "8.25", "status": "present"},
    ]
    
    fieldnames = ["id", "staff_email", "date", "clockIn", "clockOut", "hours", "status"]
    filepath = os.path.join(DATA_DIR, "attendance.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attendance)
    
    print(f"✓ Created {filepath} with {len(attendance)} attendance records")

def init_reservations():
    """Initialize reservations.csv"""
    reservations = []
    
    fieldnames = ["id", "customer_email", "date", "time", "guests", "notes", "status", "table_id", "created_at"]
    filepath = os.path.join(DATA_DIR, "reservations.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reservations)
    
    print(f"✓ Created {filepath} (empty)")

if __name__ == "__main__":
    print("Initializing CSV database...")
    print("=" * 50)
    
    init_users()
    init_menu_items()
    init_orders()
    init_order_details()
    init_tables()
    init_inventory()
    init_promotions()
    init_feedback()
    init_staff()
    init_customers()
    init_revenue()
    init_attendance()
    init_reservations()
    
    print("=" * 50)
    print("✓ Database initialization completed!")

