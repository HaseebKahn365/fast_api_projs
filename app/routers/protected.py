from fastapi import APIRouter, Depends
from app.dependencies import check_admin_privilege

router = APIRouter()

@router.get("/protected")
async def protected_endpoint(user: dict = Depends(check_admin_privilege)):
    return {"message": f"Hello {user['username']}, you have admin access!"}

