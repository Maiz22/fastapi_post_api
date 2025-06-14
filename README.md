# Social Media FastAPI
This project is a fully containerized and deployable RESTful Social Media API backend, designed with modern Python based technologies.
<br>
At its core the backend is built using Python's FastAPI with SQLModel for ORM and Pydantic for data validation. The asynchronous request handling is managed by Uvicorn, which runs under the process manager Gunicorn. The database layer uses PostgresSQL. An Nginx server acts as a reverse proxy forwarding client requests and enforcing IP-based rate limiting. Authentication has been implemented using JSON Web Tokens (JWT), with tokens being issued on a successful login, and required in request headers for certain endpoints. To further increase account security, login throttling has been implemented using a Redis database to track failed login attempts. Furthermore to improve performance, caching has been added using the same Redis database, to temporarly store response data.
<br>
The FastAPI application, SQL database, Redis, and Nginx reverse proxy are each containerized separately and managed together using Docker and Docker Compose.
<br>
The API includes interactive documentation via FastAPI's built-in Swagger UI, and the development lifecycle is managed using GIT and GitHub for version control.
This application has been successfully deployed on a Raspberry Pi with Linux as operating system. The entire stack is configured to auto start as a service via systemd in the background.
<br>

## Project Infrastructure Breakdown
This API consist of four containerized components:
- Nginx Reverse Proxy:
    - Forwarding client requests
    - IP based rate limiting
- Python FastAPI Application:
    - Asynchronous request handling
    - Response handling
    - Defining API request and response schemas
    - CRUD operations to retrive data from the PostgresDB
    - Authentication using OAuth2 and JWT
    - Password hashing
    - Cross-Origin Resource Sharing (CORS)
    - Throttling logic with Redis DB interaction
    - Caching logic with Redis DB interaction
    - Asynchronous Server Gateway Interface (ASGI) using Uvicorn
    - Process handling using Gunicorn
- Redis database:
    - Stores data for caching
    - Stores failed login attempts to implement throttling      
- Postgres SQL database:
    - SQL database storing the core data of the API
  
![Screenshot 2025-06-07 000245](https://github.com/user-attachments/assets/6041f31d-e9cb-4cb7-aff9-4a0532921d09)

## API Endpoints and Requests
- "/":
    - GET: Root endpoint displaying a simple message to the user.
- "/login":     
    - POST: Login to your account by sending username and password.
- "/users":
    - POST: Create a user account by sending email and password.
- "/users/{id}":
    - GET🔒: Retrieve user information.
- "/posts":
    - GET: Get all posts.
    - POST🔒: Create a new post.
- "/posts/{id}":
    - GET: Get a single post by its id.
    - PUT🔒: Update a post by id. Currently implemented as a PATCH, since not all fields need to be updated.
    - DELETE🔒: Delete a post by id.
- "/votes":
    - POST🔒: Upvote or downvote a post depending on vote direction send in the request body.
- "/comments":
    - POST🔒: Write a comment for a specific post.
- "/comments/{id}":
    - DELETE🔒: Delete a comment.

## Application Deployment 

This section provides a brief overview of how to deploy the application on a Raspberry Pi or a similar Linux-based device.
<br>
Since all parts of this application are containerized and managed using Docker and Docker Compose, you first need to install the Docker Engine. Please refer to the official installation guide [here](https://docs.docker.com/engine/install/ubuntu/). Additionally, in order to clone this repository, you need to install Git using the APT package manager via the command line. To do this enter the following commands: 
```
sudo apt update
sudo apt install git
```
The application will be deployed inside `/opt/myapi`, since the `/opt` directory is intended for third-party applications. Clone the repository inside `/opt/myapi` using:
```
git clone https://github.com/Maiz22/fastapi_post_api.git
```
After all files have been successfully downloaded, you need to create a `.env` file to store all environment variables for the different containers. Use the `.env.example` file to get all the necessary information.
<br>
The next step is to build your Docker images and create and run the Docker containers. To do this in one step, use the command:
```
docker compose up --build
```
Docker will now create four containers according to the rules defined in the Dockerfile and docker-compose.yml file. The API is now up and running.
<br>
You can test the application by sending requests to the different endpoints using the Swagger UI or a tool like Postman. To see the API documentation (Swagger UI) , just enter:
```
http://<device-ip-address>/docs
```
Additionally, if you want to run this application as a service that starts automatically whenever your device boots up, do the following:
<br>
Create a systemd service file inside `/etc/systemd/system/myapp.servic`. Create a `myapp.service` file that looks like this:
```
[Unit]
Description=MyApp Docker Compose Service
After=network.target docker.service
Requires=docker.service

[Service]
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/docker compose up --build
ExecStop=/usr/bin/docker compose down
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Then run the following commands:
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
```
Your API now starts inside a service every time your device boots up.

## Additional Considerations
Although this API is well-structured, incorporates many security measures, and is easily scalable, there are still a few important considerations to address before deploying it beyond your home network:
- Ensure all HTTP traffic is encrypted by implementing SSL/TLS certificates. This can be done at the Nginx reverse proxy level.
- Set short lifetimes to your JWT tokens.
- Properly setup CORS since it is currently open for all domains.
- Set additional security headers in Nginx (e.g. "Strict-Transport-Security", "Content-Security-Policy")
- If more performance is needed, implement Load Balancing using Nginx and multiple FastAPI application instances.
- Setup proper logging and monitoring 
