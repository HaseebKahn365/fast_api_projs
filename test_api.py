import requests
import json

# Test the API
base_url = "http://localhost:8000"

print("Testing FastAPI Application...")

# Test root endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"Root endpoint: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Request ID header: {response.headers.get('x-request-id')}")
except Exception as e:
    print(f"Error testing root: {e}")

# Test search endpoint (rate limiting)
print("\nTesting rate limiting...")
for i in range(7):
    try:
        response = requests.get(f"{base_url}/search?query=test{i}")
        print(f"Search {i+1}: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error on search {i+1}: {e}")

# Test CORS
print("\nTesting CORS...")
try:
    response = requests.options(f"{base_url}/",
                               headers={"Origin": "http://localhost:3000"})
    print(f"CORS preflight: {response.status_code}")
    print(f"Allow-Origin: {response.headers.get('access-control-allow-origin')}")
except Exception as e:
    print(f"Error testing CORS: {e}")

# Test webhook
print("\nTesting webhook...")
payload = {"event": "payment.success", "amount": 100}
signature = "invalid_signature"  # Wrong signature
try:
    response = requests.post(f"{base_url}/webhooks/payment",
                           json=payload,
                           headers={"X-Signature": signature})
    print(f"Webhook (invalid sig): {response.status_code}")
except Exception as e:
    print(f"Error testing webhook: {e}")

print("\nTesting complete!")