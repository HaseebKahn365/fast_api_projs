from fastapi import Depends, Request, HTTPException

def get_current_user(request: Request) -> dict:
    """Simulate getting current user from token/session"""
    # In real app, this would decode JWT or check session
    user = {"id": 1, "username": "testuser", "role": "admin"}
    return user

# nested dependency
def check_admin_privilege(user: dict = Depends(get_current_user)) -> dict:
    """Nested dependency that checks for admin privileges"""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user