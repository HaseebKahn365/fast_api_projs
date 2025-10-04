
### 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

3. **Access the API:**
   - Root endpoint: `http://127.0.0.1:8000/`
   - API documentation: `http://127.0.0.1:8000/docs`

### 🎯 My Project Objectivetion Control & Security 🔒

I'm developing a new set of features for my FastAPI project focused entirely on **application control, security, and structured code organization**. This phase introduces **Dependency Injection** for better modularity, **Custom Middleware** for centralized processing and deep control, **Rate Limiting** for protecting my endpoints from abuse, and **Webhooks** for secure, event-driven communication.

***
### �️ Project Structure

The project is now properly modularized:

```
app/
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── dependencies.py      # Dependency injection functions
├── middleware.py        # All middleware classes
├── routers/             # API route handlers
│   ├── root.py
│   ├── search.py
│   ├── protected.py
│   └── webhooks.py
└── utils/               # Utility functions
    └── rate_limiter.py
tests/
├── test_main.py         # Unit tests
requirements.txt         # Python dependencies
```

### ��� My Project Objective

My goal is to elevate the application's architecture by implementing robust control and communication mechanisms. Upon completion, my application demonstrates:

1.  **Modular Logic:** Use of **Dependency Injection (DI)** to manage shared resources and logic, especially in complex, nested scenarios.
2.  **Deep Middleware Control:** The ability to create **low-level ASGI middleware** for fundamental request/response handling and specific middleware for **response modification** and **CORS**.
3.  **Endpoint Protection:** Implementation of a **Rate Limiter** to control requests per client, enhancing security and reliability.
4.  **Event-Driven Communication:** Implementation of secure **Webhooks** for communicating asynchronous events to external services.

---

### 🧱 Architectural Components & Tasks

I implement the following tasks, focusing on sophisticated architectural patterns. I **do not** create a virtual environment.

| Task Title | Description | Attractive & Useful Usecase | Key Technologies & Concepts |
| :--- | :--- | :--- | :--- |
| **Implementing Dependency Injection** | I define reusable "dependable" functions to inject settings, database sessions, or even other dependencies into my route handlers. I implement **nested dependencies** where one dependency relies on another. | **Securing User Roles:** A dependency that retrieves the current user, which is then passed to a **nested dependency** that checks for **`admin`** or **`premium`** privileges before granting access to a resource. | `Depends()`, Global Dependencies, Nested Dependencies, Singleton Pattern. |
| **Creating Custom Middleware (High-Level)** | I implement a custom middleware function to capture client IP and response status on every API call. | **Client-Specific Audit Logging:** A middleware that automatically captures the client's IP address, the endpoint requested, and the response status code for every API call for centralized logging. | `@app.middleware("http")`, `starlette` Middleware. |
| **Creating Custom ASGI Middleware** | I explore the low-level **ASGI specification** by building middleware directly from scratch, giving me fundamental control over the request/response cycle. | **Request ID Generation:** A low-level middleware that assigns a unique **`X-Request-ID`** header to every incoming request, which is then used across all logs and downstream services for full request tracing. | ASGI Protocol, `scope`, `receive`, `send` functions, Custom ASGI Application. |
| **Developing Middleware for Response Modification** | I develop middleware specifically to intercept and alter the response body or headers before they are sent back to the client. | **Unified Response Envelope:** Middleware that ensures all successful JSON responses are wrapped in a standard format, such as `{"status": "success", "data": ...}`, standardizing client handling. | Response Interception, Body Streaming, Header Modification. |
| **Handling CORS with Middleware** | I implement the necessary middleware to securely handle **Cross-Origin Resource Sharing (CORS)** requests, allowing my frontend application to access the API from a different domain. | **Secure Frontend Access:** Configuring the middleware to only allow specific origins (my frontend URL) and specific HTTP methods (GET, POST) to prevent unauthorized domain access. | `CORSMiddleware` (from Starlette/FastAPI), Allowed Origins, Methods, Headers. |
| **Implementing Rate Limiting** | I integrate a rate-limiting mechanism to restrict the number of calls per client IP or authenticated user, targeting high-cost or sensitive endpoints. | **Protecting the Search API:** Limiting unauthenticated users to only 5 search queries per minute, preventing Denial-of-Service (DoS) attacks on my resource-intensive **Elasticsearch** service. | **Redis**, `fastapi-limiter` (or similar), Fixed Window Algorithm. |
| **Creating Webhooks in FastAPI** | I set up specific endpoints designed to receive asynchronous event notifications from external services, and I create the necessary logic to verify the source. | **Payment Gateway Integration:** Creating an endpoint (`/webhooks/payment`) to securely receive real-time notifications from a payment provider (e.g., Stripe) when a transaction is successful, updating the order status without polling. | **`POST`** Route Definition, Payload Signature Verification (Security), Asynchronous Processing. |

---

### 🛠️ Key Dependencies I Use

I utilize specialized tools for security, communication, and control flow.

| Dependency | Purpose in this Project |
| :--- | :--- |
| `fastapi-limiter` (or similar) | Used to implement the **rate-limiting** logic. |
| `redis` (client) | The backend for storing rate limit counters and potentially other cache data. |
| `python-multipart` | Handles form data, often used in `POST` requests and Webhooks. |
| Standard FastAPI/Starlette | The built-in Dependency Injection and Middleware systems, including `CORSMiddleware`. |

---

### ⚙️ Demo & Testing Strategy

My testing strategy validates that the control mechanisms are correctly intercepting and executing their tasks in the request/response flow.

1.  **CORS Test:** I test an API call from an unauthorized origin (domain) and confirm it is blocked by the browser/API with a CORS error, and then confirm a call from the **authorized origin** succeeds.
2.  **Rate Limiting Test:** I send multiple requests to a protected endpoint quickly and verify the **6th request returns a 429 Too Many Requests** status code.
3.  **Webhook Test:** I use a tool like **Postman** or a local Webhook simulator to send a valid, signed payload to my webhook endpoint and verify the application logs the successful receipt and processing of the event.
4.  **Middleware Chain Test:** I check the application logs to ensure that the **Request ID** is present in the logs created by my high-level **Audit Logging Middleware**, proving the ASGI middleware ran first.

