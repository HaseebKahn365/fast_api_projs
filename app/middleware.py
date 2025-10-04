from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import uuid
import json

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for audit logging of requests"""
    async def dispatch(self, request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        endpoint = request.url.path

        response = await call_next(request)

        # Log the audit information
        print(f"AUDIT: Client IP {client_ip} accessed {endpoint} - Status: {response.status_code}")

        return response

class RequestIDMiddleware:
    """ASGI middleware for adding request IDs"""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request_id = str(uuid.uuid4())
            headers = dict(scope.get("headers", []))
            # Add X-Request-ID header
            scope["headers"] = list(headers.items()) + [(b"x-request-id", request_id.encode())]

        await self.app(scope, receive, send)

class ResponseModificationMiddleware(BaseHTTPMiddleware):
    """Middleware for modifying response format"""
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Only modify JSON responses
        if hasattr(response, 'body') and response.media_type == 'application/json':
            # Wrap successful responses in standard envelope
            if 200 <= response.status_code < 300:
                original_body = response.body
                try:
                    data = json.loads(original_body.decode())
                    wrapped_data = {"status": "success", "data": data}
                    response.body = json.dumps(wrapped_data).encode()
                    response.headers["content-length"] = str(len(response.body))
                except:
                    pass  # If not valid JSON, leave as is

        return response

def setup_cors_middleware(app):
    """Setup CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URLs
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )