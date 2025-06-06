# Social Media FastAPI
This project is a fully containerized and deployable RESTful Social Media API backend. At its core the backend is built using Python's FastAPI with SQLModel for ORM and Pydantic for data validation. The asynchronous request handling is managed by Uvicorn, which runs under the process manager Gunicorn. The database layer uses PostgresSQL. An Nginx server acts as a reverse proxy forwarding client requests and enforcing IP-based rate limiting. Authentication has been implemented using JSON Web Tokens (JWT), with Tokens being issued on a successful login, and required in request headers for certain endpoints. To further increase account security, login throttling has been implemented using a Redis database to track failed login attempts. Furthermore to improve performance, caching has been implemented using the same Redis database.
<br>
The FastAPI application, SQL database, Redis, and Nginx reverse proxy are each containerized separately and managed together using Docker and Docker Compose.
<br>
This application has been successfully deployed on a Raspberry Pi with Linux as operating system. The entire stack is configured to auto start as a service via systemd in the background.
<br>
(Load balancing and HTTP encryption via TLS/SSL handshake have not been implemented since the project has been deployed in a private network on a single server.)


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

## Project Structure
![Screenshot 2025-06-07 000245](https://github.com/user-attachments/assets/6041f31d-e9cb-4cb7-aff9-4a0532921d09)

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

## Deployment
