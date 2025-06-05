# Social Media FastAPI

## Full Stack Description
-  Backend: FastAPI (Python) with SQLModel for ORM and Pydantic-based data validation.
-  ASGI Server: Uvicorn for handling asynchronous requests.
-  Process Management: Gunicorn running Uvicorn workers.
-  Database: PostgreSQL, containerized via Docker.
-  Web Server (Reverse Proxy): Containerized Nginx, acting as a reverse proxy and static file server. Configured with IP based rate limiting.
-  Login Throttling: Failed login attempts are tracked and throttled using a Redis-backed mechanism..
-  Containerization & Orchestration: Docker & Docker Compose for multi-container application lifecycle management.
-  Deployment Environment: Raspberry Pi running Linux, configured to auto-start the stack as a background system service with systemd.

## API Endpoints
