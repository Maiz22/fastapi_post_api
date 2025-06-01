from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from .routers import root, posts, users, auth, votes

if TYPE_CHECKING:
    from typing import AsyncGenerator, Any


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    Defines the startup and shutdown logic of our API.
    """
    ### Startup logic

    # Setup database
    create_db_and_tables()

    # Add middleware
    # origins = [
    #    "http://localhost.tiangolo.com",
    #    "https://localhost.tiangolo.com",
    #    "http://localhost",
    #    "http://localhost:8000",
    # ]
    # app.add_middleware(
    #    CORSMiddleware,
    #    allow_origins=origins,
    #    allow_credentials=True,
    #    allow_methods=["*"],
    #    allow_headers=["*"],
    # )

    # Setup routes
    app.include_router(router=root.router, prefix="", tags=["Root"])
    app.include_router(router=auth.router, tags=["Authentication"])
    app.include_router(router=users.router, prefix="/users", tags=["Users"])
    app.include_router(router=posts.router, prefix="/posts", tags=["Posts"])
    app.include_router(router=votes.router, prefix="/votes", tags=["Votes"])

    yield

    ### Shutdown logic


# Create fast api main instance
app = FastAPI(lifespan=lifespan)
