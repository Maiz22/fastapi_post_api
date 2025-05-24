from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from .routers import root, posts

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

    # Setup routes
    app.include_router(router=root.router, prefix="", tags=["root"])
    app.include_router(router=posts.router, prefix="/posts", tags=["posts"])

    yield

    ### Shutdown logic


# Create fast api main instance
app = FastAPI(lifespan=lifespan)
