from fastapi import FastAPI
from app.routers import auth, items, files
from app.config.database import engine
from app.models.sql_models import Base
import asyncio
import uvicorn

app = FastAPI(title="Advanced Data Management API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(items.router, prefix="/api", tags=["items"])
app.include_router(files.router, prefix="/files", tags=["files"])

@app.on_event("startup")
async def startup_event():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Advanced Data Management API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)