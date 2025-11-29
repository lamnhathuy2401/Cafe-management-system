"""
Authentication and authorization utilities
Provides decorators and dependencies for role-based access control
"""
from functools import wraps
from fastapi import Request, HTTPException, Depends
from typing import Optional, List
import database as db
from constants import UserRole


def get_current_user(request: Request) -> Optional[dict]:
    """
    Get current authenticated user from session
    
    Args:
        request: FastAPI request object
        
    Returns:
        User dict if authenticated, None otherwise
    """
    user_email = request.session.get("user_email")
    if user_email:
        user = db.find_one("users.csv", "email", user_email)
        return user
    return None


def require_auth(func):
    """
    Decorator to require authentication
    
    Usage:
        @app.get("/api/endpoint")
        @require_auth
        async def my_endpoint(request: Request):
            # user is guaranteed to be authenticated
            pass
    """
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        # Inject user into kwargs
        kwargs['user'] = user
        return await func(request, *args, **kwargs)
    return wrapper


def require_role(allowed_roles: List[str]):
    """
    Decorator to require specific role(s)
    
    Args:
        allowed_roles: List of allowed roles (e.g., ["manager", "staff"])
    
    Usage:
        @app.post("/api/menu-items")
        @require_role([UserRole.MANAGER])
        async def create_menu_item(request: Request):
            # Only managers can access
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user = get_current_user(request)
            if not user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            if user.get("role") not in allowed_roles:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            # Inject user into kwargs
            kwargs['user'] = user
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


# FastAPI Dependencies (alternative to decorators)
def get_authenticated_user(request: Request) -> dict:
    """
    FastAPI dependency to get authenticated user
    
    Usage:
        @app.get("/api/endpoint")
        async def my_endpoint(user: dict = Depends(get_authenticated_user)):
            # user is guaranteed to be authenticated
            pass
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def require_manager_role(request: Request) -> dict:
    """
    FastAPI dependency to require manager role
    
    Usage:
        @app.post("/api/menu-items")
        async def create_menu_item(
            user: dict = Depends(require_manager_role)
        ):
            # Only managers can access
            pass
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.get("role") != UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Manager access required")
    return user


def require_staff_or_manager_role(request: Request) -> dict:
    """
    FastAPI dependency to require staff or manager role
    
    Usage:
        @app.post("/api/create-order")
        async def create_order(
            user: dict = Depends(require_staff_or_manager_role)
        ):
            # Staff and managers can access
            pass
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.get("role") not in [UserRole.STAFF, UserRole.MANAGER]:
        raise HTTPException(
            status_code=403, 
            detail="Staff or manager access required"
        )
    return user


def require_customer_role(request: Request) -> dict:
    """
    FastAPI dependency to require customer role
    
    Usage:
        @app.post("/api/customer/create-order")
        async def customer_create_order(
            user: dict = Depends(require_customer_role)
        ):
            # Only customers can access
            pass
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.get("role") != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Customer access required")
    return user

