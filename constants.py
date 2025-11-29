"""
Constants for the Coffee Manager application
Replaces magic strings and numbers throughout the codebase
"""


class UserRole:
    """User role constants"""
    CUSTOMER = "customer"
    STAFF = "staff"
    MANAGER = "manager"


class TableStatus:
    """Table status constants"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class OrderStatus:
    """Order status constants"""
    PENDING = "pending"
    IN_PREPARATION = "in_preparation"
    COMPLETED = "completed"
    WAITING_PAYMENT = "waiting_payment"


class PaymentStatus:
    """Payment status constants"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class PaymentMethod:
    """Payment method constants"""
    CASH = "cash"
    CARD = "card"
    E_WALLET = "e_wallet"


class ReservationStatus:
    """Reservation status constants"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class FeedbackStatus:
    """Feedback status constants"""
    PENDING = "pending"
    RESPONDED = "responded"


class MenuItemStatus:
    """Menu item status constants"""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class PromotionStatus:
    """Promotion status constants"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class StaffStatus:
    """Staff status constants"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class OrderPrefix:
    """Order ID prefixes"""
    ORDER = "ORD-"
    RESERVATION = "RES-"
    IMPORT = "IMP-"
    EXPORT = "EXP-"
    TRANSACTION = "TXN-"


class AttendanceStatus:
    """Attendance status constants"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


# Session keys
class SessionKey:
    """Session key constants"""
    USER_EMAIL = "user_email"
    ROLE = "role"


# Default values
class Defaults:
    """Default values"""
    DEFAULT_PASSWORD = "123456"
    DEFAULT_MENU_STATUS = MenuItemStatus.AVAILABLE
    DEFAULT_PROMOTION_STATUS = PromotionStatus.ACTIVE
    DEFAULT_STAFF_STATUS = StaffStatus.ACTIVE

