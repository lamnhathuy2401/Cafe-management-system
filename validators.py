"""
Validation utilities
Centralizes validation logic to avoid duplication
"""
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Union, Optional


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def validate_positive_float(value: Union[str, float, int], field_name: str = "Giá trị") -> float:
    """
    Validate that a value is a positive float
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated float value
        
    Raises:
        ValidationError: If value is not a valid positive float
    """
    try:
        value = float(value)
        if value < 0:
            raise ValidationError(f"{field_name} phải là số dương")
        return value
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} phải là số")


def validate_non_negative_float(value: Union[str, float, int], field_name: str = "Giá trị") -> float:
    """
    Validate that a value is a non-negative float (allows 0)
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated float value
        
    Raises:
        ValidationError: If value is not a valid non-negative float
    """
    try:
        value = float(value)
        if value < 0:
            raise ValidationError(f"{field_name} không được là số âm")
        return value
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} phải là số")


def validate_required(value: Optional[str], field_name: str) -> str:
    """
    Validate that a required field is not empty
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated string value
        
    Raises:
        ValidationError: If value is empty or None
    """
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"Vui lòng điền {field_name}")
    return value.strip() if isinstance(value, str) else str(value)


def validate_email(email: str) -> str:
    """
    Validate email format
    
    Args:
        email: Email to validate
        
    Returns:
        Validated email string
        
    Raises:
        ValidationError: If email format is invalid
    """
    email = email.strip()
    if "@" not in email or "." not in email.split("@")[1]:
        raise ValidationError("Email không hợp lệ")
    return email


def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d", field_name: str = "Ngày") -> datetime:
    """
    Validate date format
    
    Args:
        date_str: Date string to validate
        format_str: Expected date format
        field_name: Name of the field for error messages
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValidationError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        raise ValidationError(f"Định dạng {field_name.lower()} không hợp lệ ({format_str})")


def validate_datetime_format(
    date_str: str, 
    time_str: str, 
    date_format: str = "%Y-%m-%d",
    time_format: str = "%H:%M",
    field_name: str = "Ngày/giờ"
) -> datetime:
    """
    Validate datetime format (date + time)
    
    Args:
        date_str: Date string
        time_str: Time string
        date_format: Expected date format
        time_format: Expected time format
        field_name: Name of the field for error messages
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValidationError: If datetime format is invalid
    """
    try:
        return datetime.strptime(f"{date_str} {time_str}", f"{date_format} {time_format}")
    except ValueError:
        raise ValidationError(f"Định dạng {field_name.lower()} không hợp lệ")


def validate_future_datetime(dt: datetime, field_name: str = "Thời gian") -> datetime:
    """
    Validate that datetime is in the future
    
    Args:
        dt: Datetime to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated datetime
        
    Raises:
        ValidationError: If datetime is in the past
    """
    if dt < datetime.now():
        raise ValidationError(f"Vui lòng chọn {field_name.lower()} trong tương lai")
    return dt


def validate_date_range(start_date: datetime, end_date: datetime) -> tuple:
    """
    Validate that end date is after start date
    
    Args:
        start_date: Start datetime
        end_date: End datetime
        
    Returns:
        Tuple of (start_date, end_date)
        
    Raises:
        ValidationError: If end date is before start date
    """
    if end_date < start_date:
        raise ValidationError("Thời gian kết thúc phải sau thời gian bắt đầu")
    return start_date, end_date


def validate_positive_integer(value: Union[str, int], field_name: str = "Số lượng") -> int:
    """
    Validate that a value is a positive integer
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated integer value
        
    Raises:
        ValidationError: If value is not a valid positive integer
    """
    try:
        value = int(value)
        if value <= 0:
            raise ValidationError(f"{field_name} phải là số nguyên dương")
        return value
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} phải là số nguyên")


def validate_enum(value: str, allowed_values: list, field_name: str = "Giá trị") -> str:
    """
    Validate that a value is in a list of allowed values
    
    Args:
        value: Value to validate
        allowed_values: List of allowed values
        field_name: Name of the field for error messages
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If value is not in allowed values
    """
    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} không hợp lệ. Giá trị cho phép: {', '.join(allowed_values)}"
        )
    return value


def handle_validation_error(error: ValidationError) -> JSONResponse:
    """
    Convert ValidationError to JSONResponse
    
    Args:
        error: ValidationError instance
        
    Returns:
        JSONResponse with error message
    """
    return JSONResponse(
        {
            "success": False,
            "message": error.message
        },
        status_code=error.status_code
    )

