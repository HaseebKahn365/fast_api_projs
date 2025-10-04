## Project: Real-Time Communication and Secure File Service 💬

I am developing the next major iteration of my FastAPI application, focusing on **real-time communication** via WebSockets, **secure authentication**, and robust **file transfer** capabilities. This project integrates the high-performance aspects of WebSockets for a dynamic user experience while maintaining the security standards established previously.

***

### 🎯 My Project Objective

My goal is to build a high-performance backend that supports both traditional $\text{HTTP}$ and real-time $\text{WebSocket}$ interactions. Upon completion, my application demonstrates:

1.  **Real-Time Chat:** A persistent, global chat room that instantly broadcasts messages to all connected users and stores chat history.
2.  **Secure Session Management:** Use of $\text{HTTP}$-Only cookies for JWT-based session authentication for both $\text{HTTP}$ and $\text{WebSocket}$ connections.
3.  **File Management:** Endpoints for secure file uploads and the generation of dedicated download links.
4.  **Performance and Scalability:** Efficient handling of continuous $\text{WebSocket}$ connections and optimized history retrieval.

---

### 🧱 Architectural Components & Tasks

I implement the following tasks, primarily located in new routers (`ws.py`, `files.py`), a database module (`database.py`), and a new $\text{WebSocket}$ manager utility. I **do not** use Redis, opting for an **SQLite database** for persistent chat state. I **do not** create a virtual environment.

| Task Title | Description | Key Technologies & Concepts |
| :--- | :--- | :--- |
| **Setting up Websockets in FastAPI** | I define the foundational $\text{WebSocket}$ endpoint and the manager class responsible for handling concurrent connections. | `WebSocket` class, $\text{ASGI}$ Communication, $\text{WebSocket}$ endpoint decorator (`@router.websocket`). |
| **Sending and receiving messages over WebSockets** | I implement the core send/receive loop in the $\text{WebSocket}$ handler function to allow bidirectional communication. | `websocket.receive_text()`, `websocket.send_text()`, `async/await` for I/O. |
| **Handling WebSocket connections and disconnections** | I implement logic within the $\text{WebSocket}$ manager to track active clients and gracefully handle abrupt connection closures. | `manager.connect()`, `manager.disconnect()`, $\text{Exception}$ handling within the $\text{WebSocket}$ loop. |
| **Handling WebSocket errors and exceptions** | I define custom error handling within the $\text{WebSocket}$ loop to send informative error codes/messages back to the client before closing the connection. | Custom $\text{WebSocket}$ Close Codes, `try...except` blocks for clean teardown. |
| **Implementing global chat functionality** | I create a **global chat room** using an SQLite database to store the chat history persistently. | **SQLite storage** (messages table), Broadcast loop (`manager.broadcast()`). |
| **Retrieving Chat History (Last 20)** | I create an $\text{HTTP GET}$ endpoint that efficiently returns the **last $\text{20}$ messages** from the SQLite database. | $\text{HTTP GET}$ route, SQL query with LIMIT, **Pydantic** Response Model. |
| **Retrieving Chat History (Offset/Limit)** | I create another $\text{HTTP GET}$ endpoint that accepts **query parameters** (`offset` and `limit`) to deliver older messages in batches. | Query Parameters, SQL OFFSET and LIMIT, Data Pagination logic. |
| **Securing WebSocket connections with OAuth2 (JWT)** | I adapt the $\text{HTTP}$ dependency to read the $\text{JWT}$ from the **$\text{HTTP}$-Only cookie** or query parameter and authenticate the user *before* accepting the $\text{WebSocket}$ connection. | **Cookie or Query Authentication in WebSockets**, $\text{JWT}$ validation, Manual auth check in $\text{WebSocket}$ function. |
| **User Registration** | I create a $\text{POST}$ endpoint for user registration with username and password. | Password hashing with bcrypt, SQLite user storage. |
| **Working with file uploads** | I create a $\text{POST}$ endpoint to securely receive binary file data and save it to the local filesystem (or a temporary store). | $\text{FastAPI}$ `File` and `UploadFile`, Asynchronous file I/O (`await file.write()`). |
| **Creating a download link** | I create a $\text{GET}$ endpoint that serves the saved file by filename, returning it as a **`FileResponse`** or **`StreamingResponse`**. | `FileResponse` or `StreamingResponse`, Security check (e.g., authenticated user), $\text{Content-Disposition}$ header for filename. |

---

### ⚙️ Demo & Testing Strategy

Testing this project requires validating both $\text{HTTP}$ and $\text{WebSocket}$ protocols. The app runs on `http://127.0.0.1:8001` with data stored in `chat_app.db`.

1.  **Authentication Test:**
    * Register a user via `/register` (POST with JSON `{"username": "test", "password": "pass"}`).
    * Log in via `/token` (POST with form `username=test&password=pass`) and verify the **$\text{HTTP}$-Only cookie** is set.
    * Connect to the $\text{WebSocket}$ at `ws://127.0.0.1:8001/ws/chat?token=<jwt>` (or use cookie) and verify success. Invalid tokens reject the connection.
2.  **Chat Functionality Test:**
    * Connect two clients to `ws://127.0.0.1:8001/ws/chat?token=<jwt>`.
    * Send plain text messages (e.g., "Hello") from Client A; Client B receives instantly.
    * Disconnect Client B, send more messages from Client A, reconnect Client C, and query `/history/last20` (GET, authenticated) to verify stored messages.
3.  **File Transfer Test:**
    * Use **Swagger $\text{UI}$** at `/docs` to upload a file via `/files/upload` (authenticated).
    * Verify the response provides a download URL.
    * Access the URL to download the file with original name.

The use of $\text{HTTP}$-Only cookies or query tokens ensures secure sessions. History endpoints require authentication for data privacy.