"""Database tests against the throwaway PostgreSQL started in conftest.py."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from ecommerce.core.db import database_info, get_db, get_engine
from ecommerce.main import app


def test_connects_to_the_test_database_with_the_ecomm_schema() -> None:
    info = database_info(get_engine())

    assert info.version.startswith("18")
    assert info.database == "ecomm_db"
    assert info.schema == "ecomm"  # search_path from ecomm-setup.sql
    assert info.products == 0  # tables exist, but the test database has no sample data


def test_get_db_yields_a_working_session_and_closes_it() -> None:
    sessions = get_db()
    session = next(sessions)
    assert session.execute(text("SELECT 1")).scalar() == 1

    sessions.close()  # what FastAPI does after the response: runs the `finally` block

    assert not session.in_transaction()


def test_health_is_down_with_503_when_the_database_is_unreachable(client: TestClient) -> None:
    # Nothing listens on port 1; connect_timeout keeps the attempt short
    unreachable = create_engine(
        "postgresql+psycopg://postgres:password@127.0.0.1:1/ecomm_db",
        connect_args={"connect_timeout": 1},
    )
    app.dependency_overrides[get_engine] = lambda: unreachable
    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"status": "DOWN", "components": {"db": "DOWN"}}
