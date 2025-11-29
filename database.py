"""
Database module using CSV files for data storage
"""
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime

# Data directory
DATA_DIR = "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def get_csv_path(filename: str) -> str:
    """Get full path to CSV file"""
    return os.path.join(DATA_DIR, filename)

def read_csv(filename: str) -> List[Dict]:
    """Read data from CSV file"""
    filepath = get_csv_path(filename)
    if not os.path.exists(filepath):
        return []
    
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []
    
    return data

def write_csv(filename: str, data: List[Dict], fieldnames: List[str]):
    """Write data to CSV file"""
    filepath = get_csv_path(filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        raise

def append_csv(filename: str, row: Dict, fieldnames: List[str]):
    """Append a row to CSV file"""
    filepath = get_csv_path(filename)
    file_exists = os.path.exists(filepath)
    
    try:
        with open(filepath, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Error appending to {filename}: {e}")
        raise

def update_csv(filename: str, key_field: str, key_value: str, updates: Dict, fieldnames: List[str]):
    """Update a row in CSV file"""
    data = read_csv(filename)
    
    for i, row in enumerate(data):
        if row.get(key_field) == key_value:
            data[i].update(updates)
            break
    
    write_csv(filename, data, fieldnames)

def delete_csv(filename: str, key_field: str, key_value: str, fieldnames: List[str]):
    """Delete a row from CSV file"""
    data = read_csv(filename)
    data = [row for row in data if row.get(key_field) != key_value]
    write_csv(filename, data, fieldnames)

def find_one(filename: str, key_field: str, key_value: str) -> Optional[Dict]:
    """Find one record by key"""
    data = read_csv(filename)
    for row in data:
        if row.get(key_field) == key_value:
            return row
    return None

def find_many(filename: str, filter_func=None) -> List[Dict]:
    """Find multiple records with optional filter"""
    data = read_csv(filename)
    if filter_func:
        data = [row for row in data if filter_func(row)]
    return data


class CSVSchemas:
    """
    CSV fieldnames schemas to avoid duplication
    Centralizes all CSV column definitions
    """
    # Users
    USERS = ["id", "name", "email", "password", "phone", "role"]
    
    # Menu Items
    MENU_ITEMS = ["id", "name", "category", "price", "image", "description", "status"]
    
    # Orders
    ORDERS = [
        "id", "customer_email", "customer_name", "date", "total", "status",
        "payment_method", "payment_status", "table_id", "created_at"
    ]
    
    # Order Details
    ORDER_DETAILS = ["order_id", "menu_item_id", "quantity", "price", "subtotal"]
    
    # Tables
    TABLES = ["id", "number", "capacity", "status"]
    
    # Inventory
    INVENTORY = ["id", "name", "quantity", "unit", "minStock", "supplier"]
    
    # Promotions
    PROMOTIONS = [
        "id", "code", "name", "description", "discount", "type",
        "maxDiscount", "minOrder", "startDate", "endDate", "status"
    ]
    
    # Feedback
    FEEDBACK = [
        "id", "customer_email", "customer_name", "date", "foodRating",
        "serviceRating", "comment", "status", "response"
    ]
    
    # Staff
    STAFF = ["id", "name", "role", "email", "phone", "status", "schedule"]
    
    # Customers
    CUSTOMERS = ["id", "name", "email", "phone", "totalOrders", "totalSpent", "status"]
    
    # Revenue
    REVENUE = ["date", "revenue", "orders"]
    
    # Attendance
    ATTENDANCE = ["id", "staff_email", "date", "clockIn", "clockOut", "hours", "status"]
    
    # Reservations
    RESERVATIONS = [
        "id", "customer_email", "date", "time", "guests", "notes",
        "status", "table_id", "created_at"
    ]
