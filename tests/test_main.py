import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": {"message": "Advanced FastAPI Application"}}

def test_protected_endpoint_admin():
    # Mock admin user - in real app, you'd use test tokens
    response = client.get("/protected")
    # Since we don't have auth setup in tests, this will fail with 403
    # But the middleware should still wrap the response
    assert response.status_code == 403
    assert "detail" in response.json()

def test_search_endpoint():
    response = client.get("/search?query=test")
    assert response.status_code == 200
    assert "results" in response.json()["data"]

def test_cors_headers():
    response = client.options("/",
                           headers={"Origin": "http://localhost:3000",
                                   "Access-Control-Request-Method": "GET"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_unauthorized_cors():
    response = client.options("/",
                           headers={"Origin": "http://evil.com",
                                   "Access-Control-Request-Method": "GET"})
    # CORS should block this
    assert "access-control-allow-origin" not in response.headers

def test_rate_limiting():
    # Send multiple requests to test rate limiting
    for i in range(6):
        response = client.get("/search?query=test")
        if i < 5:
            assert response.status_code == 200
        else:
            # 6th request should be rate limited
            assert response.status_code == 429

def test_webhook_invalid_signature():
    payload = {"event": "payment.success", "amount": 100}
    import json
    import hmac
    import hashlib

    # Wrong secret
    wrong_signature = hmac.new(b"wrong_secret", json.dumps(payload).encode(), hashlib.sha256).hexdigest()

    response = client.post("/webhooks/payment",
                          json=payload,
                          headers={"X-Signature": wrong_signature})
    assert response.status_code == 401

def test_request_id_middleware():
    response = client.get("/")
    # Check if X-Request-ID header is present in response
    assert "x-request-id" in response.headers