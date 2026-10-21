"""Shared pytest setup: pytest loads this file before any test module.

main.py reads settings when it is imported, so the test environment must be set
here, at the top, before any test imports ecommerce.main.

Tests get a throwaway PostgreSQL 18 in Docker (Testcontainers), built from the same
db/scripts/ecomm-setup.sql as the real databases, so they never touch local or Docker data.
Docker Desktop must be running.
"""

import os
import time
from collections.abc import Iterator
from pathlib import Path

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from testcontainers.community.postgres import PostgresContainer

SETUP_SQL = Path(__file__).resolve().parents[2] / "db" / "scripts" / "ecomm-setup.sql"

# One container for the whole test session (like Spring reusing it per context)
_postgres = PostgresContainer(
    "postgres:18", username="postgres", password="password", dbname="ecomm_db", driver="psycopg"
).with_volume_mapping(str(SETUP_SQL), "/docker-entrypoint-initdb.d/01-ecomm-setup.sql", "ro")
_postgres.start()


def _wait_until_ready(url: str, timeout_s: float = 30) -> None:
    """The image runs init scripts on a temporary server first; wait for the real one."""
    deadline = time.monotonic() + timeout_s
    engine = sqlalchemy.create_engine(url)
    try:
        while True:
            try:
                with engine.connect() as connection:
                    if connection.execute(
                        sqlalchemy.text("SELECT to_regclass('ecomm.products')")
                    ).scalar():
                        return
            except sqlalchemy.exc.OperationalError:
                pass
            if time.monotonic() > deadline:
                raise TimeoutError("test database did not become ready")
            time.sleep(0.5)
    finally:
        engine.dispose()


_wait_until_ready(_postgres.get_connection_url())

# Real environment variables override the .env files, so tests never depend on them
os.environ["APP_ENV"] = "test"
os.environ["JWT_SECRET"] = "test-secret-that-is-at-least-32-characters-long"
os.environ["DB_HOST"] = _postgres.get_container_host_ip()
os.environ["DB_PORT"] = str(_postgres.get_exposed_port(5432))
os.environ["DB_NAME"] = "ecomm_db"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"

from ecommerce.main import app  # noqa: E402  (must come after the env setup above)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Remove the test database container when the test run ends."""
    _postgres.stop()


@pytest.fixture
def clean_products() -> Iterator[None]:
    """For tests that write to the test database: empty the products table afterwards."""
    yield
    from ecommerce.core.db import get_engine

    with get_engine().begin() as connection:
        connection.execute(sqlalchemy.text("TRUNCATE ecomm.products RESTART IDENTITY CASCADE"))


@pytest.fixture
def client() -> Iterator[TestClient]:
    """An HTTP client that calls the app in-process; `with` also runs the lifespan."""
    with TestClient(app) as test_client:
        yield test_client
