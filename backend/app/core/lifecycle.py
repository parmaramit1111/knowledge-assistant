from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import close_database


@asynccontextmanager
async def lifespan(app: FastAPI):

    #
    # Startup
    #

    yield

    #
    # Shutdown
    #

    await close_database()