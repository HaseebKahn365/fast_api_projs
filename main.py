from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from auth import authenticate_user, create_access_token, register_user
from ws import router as ws_router
from files import router as files_router

app = FastAPI(title="Real-Time Communication and Secure File Service", version="1.0.0")

app.include_router(ws_router, tags=["WebSockets"])
app.include_router(files_router, tags=["Files"])

class UserRegister(BaseModel):
    username: str
    password: str

@app.post("/register", tags=["Auth"])
async def register(user: UserRegister):
    register_user(user.username, user.password)
    return {"message": "User registered successfully"}

@app.post("/token", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=86400)  # 1 day
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to the Real-Time Chat and File Service API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)