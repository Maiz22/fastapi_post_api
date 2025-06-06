# Social Media FastAPI

## Stack Description
-  Backend: Python's FastAPI with SQLModel for ORM and Pydantic-based data validation.
-  ASGI Server: Uvicorn for handling asynchronous requests.
-  Process Management: Gunicorn running Uvicorn workers.
-  Database: PostgreSQL, containerized via Docker.
-  Web Server / Reverse Proxy / Rate Limiting: Containerized Nginx, acting as a reverse proxy and static file server. Configured with IP based rate limiting.
-  Authentication: Using Json Web Token (JWT), created at login and used inside request headers for user authentication.
-  Login Throttling: Failed login attempts are tracked and throttled using a Redis-backed mechanism..
-  Containerization & Orchestration: Docker & Docker Compose for multi-container application lifecycle management.
-  Deployment Environment: Raspberry Pi running Linux, configured to auto-start the stack as a background system service with systemd.
-  API Documentation: FastAPIs interactive Swagger UI.
-  Version Control System: GIT & GitHub.

## Project Architecture

## API Endpoints and Requests
- "/":
    - GET: Root endpoint displaying a simple message to the user.
- "/login":
    - POST: Login to your account by sending username and password.
- "/users":
    - POST: Create a user account by sending email and password.
- "/users/{id}":
    - GET: Retrieve user information.
- "/posts":
    - GET: Get all posts.
    - POST: Create a new post.
- "/posts/{id}":
    - GET: Get a single post by its id.
    - PUT: Update a post by id. Currently implemented as a PATCH, since not all fields need to be updated.
    - DELETE: Delete a post by id.
- "/votes":
    - POST: Upvote or downvote a post depending on vote direction send in the request body.
- "/comments":
    - POST: Write a comment for a specific post.
- "/comments/{id}":
    - DELETE: Delete a comment.

##
