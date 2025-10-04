from fastapi import APIRouter, Request, HTTPException
import hashlib
import hmac
import json
from app.config import WEBHOOK_SECRET

router = APIRouter()

@router.post("/webhooks/payment")
async def payment_webhook(request: Request):
    """Webhook endpoint for payment notifications"""
    body = await request.body()
    signature = request.headers.get("X-Signature")

    # Verify webhook signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Process webhook payload
    payload = json.loads(body)
    print(f"WEBHOOK: Received payment event: {payload}")

    # In real app, update order status, send notifications, etc.
    return {"status": "processed"}