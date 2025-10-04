from fastapi import FastAPI
from app.middleware import (
    AuditLoggingMiddleware,
    RequestIDMiddleware,
    ResponseModificationMiddleware,
    setup_cors_middleware
)
from app.routers import root, search, protected, webhooks

app = FastAPI(title="Advanced FastAPI Application", version="1.0.0")

# Add middleware
app.add_middleware(RequestIDMiddleware)  # ASGI middleware runs first
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(ResponseModificationMiddleware)
setup_cors_middleware(app)

# Include routers
app.include_router(root.router)
app.include_router(search.router)
app.include_router(protected.router)
app.include_router(webhooks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)