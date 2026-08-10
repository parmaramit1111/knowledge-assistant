import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import close_database
from app.workers.scheduler.scheduler import Scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    #
    # Startup
    #
    scheduler = Scheduler()

    task = asyncio.create_task(
        scheduler.start(),
    )

    try:
        yield

    finally:
        #
        # Shutdown
        #
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        await close_database()