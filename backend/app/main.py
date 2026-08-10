from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.core.config import settings
from app.core.middleware import register_middlewares
from app.core.lifecycle import lifespan
from app.core.logging import setup_logging
from app.core.handlers.exception_handlers import register_exception_handlers

import app.providers.embeddings

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all exception handlers from the handlers folder
register_exception_handlers(app)

# Register all middlewares from the middlewares folder
register_middlewares(app)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }
