from fastapi import APIRouter, WebSocket, Depends, HTTPException
from jose import JWTError, jwt
from utils import manager
from models import Message
from datetime import datetime
from typing import List
from database import add_message, get_last_messages, get_messages_with_offset
from auth import get_current_user

router = APIRouter()

SECRET_KEY = "haseeb"
ALGORITHM = "HS256"

async def get_current_user_ws(websocket: WebSocket):
    token = websocket.cookies.get("access_token") or websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)  # Policy Violation
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            await websocket.close(code=1008)
            return None
    except JWTError:
        await websocket.close(code=1008)
        return None
    return username


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    user = await get_current_user_ws(websocket)
    if user is None:
        return  # Connection already closed
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_text = data.strip()
            if not message_text:
                continue
            add_message(user, message_text)
            await manager.broadcast(f"{user}: {message_text}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

@router.get("/history/last20", response_model=List[Message])
async def get_last_20_messages():
    return get_last_messages(20)

@router.get("/history", response_model=List[Message])
async def get_history(offset: int = 0, limit: int = 20, current_user: str = Depends(get_current_user)):
    if offset < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid offset or limit")
    return get_messages_with_offset(offset, limit)