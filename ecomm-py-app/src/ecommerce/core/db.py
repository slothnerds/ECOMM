"""Database access: engine (connection pool), sessions and a startup check.

The counterpart of Spring's DataSource (HikariCP) + EntityManager. The engine is created on
first use, not at import time, so tests can point the app at their own database first.
"""

from collections.abc import Generator
from dataclasses import dataclass
from functools import lru_cache

from sqlalchemy import Engine, MetaData, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ecommerce.core.config import get_settings


class Base(DeclarativeBase):
    """Parent of every ORM table class (the counterpart of JPA's @Entity).

    Tables default to schema "ecomm", created by db/scripts/ecomm-setup.sql. The script owns
    the schema: the app never runs CREATE TABLE (like Hibernate's ddl-auto: validate).
    """

    metadata = MetaData(schema="ecomm")


@lru_cache
def get_engine() -> Engine:
    """The app-wide connection pool (one per process, like a Spring singleton bean)."""
    return create_engine(
        get_settings().database_url,
        # Test a pooled connection before handing it out, so a restarted database is survived
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        # Give up connecting after N seconds; libpq waits forever by default, so an unreachable
        # database would hang startup and /health (on Windows a closed port isn't refused at once)
        connect_args={"connect_timeout": get_settings().db_connect_timeout_s},
    )


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_db() -> Generator[Session]:
    """FastAPI dependency: one session per request, always closed afterwards.

    The code after `yield` runs once the response is done, even if the endpoint raised.
    """
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


@dataclass(frozen=True, slots=True)
class DatabaseInfo:
    version: str
    port: int
    database: str
    schema: str
    products: int | None  # None if the tables haven't been created yet


def database_info(engine: Engine) -> DatabaseInfo:
    """Which server, database and schema we're connected to; raises if unreachable."""
    with engine.connect() as connection:
        row = connection.execute(
            text(
                """
                SELECT current_setting('server_version') AS version,
                       inet_server_port()               AS port,
                       current_database()               AS database,
                       current_schema()                 AS schema,
                       CASE WHEN to_regclass('ecomm.products') IS NULL THEN NULL
                            ELSE (SELECT count(*) FROM ecomm.products) END AS products
                """
            )
        ).one()
    return DatabaseInfo(
        version=row.version,
        port=row.port,
        database=row.database,
        schema=row.schema,
        products=row.products,
    )


def is_database_up(engine: Engine) -> bool:
    """Cheap liveness probe used by /health."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        return False
    return True
