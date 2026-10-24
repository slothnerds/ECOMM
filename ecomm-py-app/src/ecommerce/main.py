"""Application entry point: creates the FastAPI app (like EcommerceApplication.java)."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ecommerce.core import health
from ecommerce.core.config import get_settings
from ecommerce.core.db import database_info, get_engine
from ecommerce.core.errors import register_error_handlers
from ecommerce.product import router as product_router

# Reuse uvicorn's already-configured logger until logging is set up properly (Stage 16)
logger = logging.getLogger("uvicorn.error")

# Load settings at import time, so invalid configuration stops the app immediately
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup/shutdown hook (the counterpart of an ApplicationRunner in Spring)."""
    logger.info("Profile: %s", settings.profile)
    logger.info("Configuration loaded: %r", settings)
    logger.info("Database: %s", settings.database_display)
    # Fail fast: if the database can't be reached, this raises and the app doesn't start
    info = database_info(get_engine())
    logger.info(
        "Connected to PostgreSQL %s on port %s: database %s, schema %s, %s products",
        info.version,
        info.port,
        info.database,
        info.schema,
        "no" if info.products is None else info.products,
    )
    yield
    # Shutdown: close all pooled connections
    get_engine().dispose()


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
# One error format for every failure (core/errors.py)
register_error_handlers(app)
app.include_router(health.router)
app.include_router(product_router.router)


def run() -> None:
    """Start the dev server; used by the `ecommerce` script in pyproject.toml."""
    uvicorn.run("ecommerce.main:app", host="127.0.0.1", port=settings.port, reload=True)
