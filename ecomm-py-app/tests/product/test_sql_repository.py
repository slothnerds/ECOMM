"""SqlProductRepository against the Testcontainers PostgreSQL (real schema, ecomm-setup.sql).

The counterpart of JpaProductRepositoryTest.java. Each test empties the products table afterwards.
"""

from collections.abc import Iterator
from dataclasses import replace
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from ecommerce.core.db import get_session_factory
from ecommerce.product.models import Product, ProductStatus
from ecommerce.product.repository import SqlProductRepository

pytestmark = pytest.mark.usefixtures("clean_products")


@pytest.fixture
def session() -> Iterator[Session]:
    with get_session_factory()() as session:
        yield session


@pytest.fixture
def repository(session: Session) -> SqlProductRepository:
    return SqlProductRepository(session)


def product(sku: str) -> Product:
    return Product(sku=sku, name=f"Product {sku}", price=Decimal("9.99"))


def test_save_inserts_and_the_database_fills_generated_columns(
    repository: SqlProductRepository,
) -> None:
    saved = repository.save(product("TST-1"))

    assert saved.id is not None and saved.id > 0
    assert saved.version == 0
    assert saved.status is ProductStatus.ACTIVE
    assert saved.created_at is not None
    assert saved.price == Decimal("9.99")


def test_find_by_sku_and_find_all_ordered_by_id(repository: SqlProductRepository) -> None:
    first = repository.save(product("TST-1"))
    second = repository.save(product("TST-2"))

    assert repository.find_by_sku("TST-2") == second
    assert repository.find_by_sku("NOPE-1") is None
    assert repository.find_all() == [first, second]


def test_update_increments_the_version(repository: SqlProductRepository) -> None:
    saved = repository.save(product("TST-1"))

    updated = repository.save(replace(saved, price=Decimal("12.00")))

    assert updated.version == 1
    assert updated.price == Decimal("12.00")


def test_database_rejects_a_duplicate_sku(repository: SqlProductRepository) -> None:
    repository.save(product("TST-1"))

    # The service checks first, but the unique constraint is the real guarantee (e.g. under races)
    with pytest.raises(IntegrityError, match="products_sku_uq"):
        repository.save(product("TST-1"))


def test_database_rejects_a_non_positive_price(repository: SqlProductRepository) -> None:
    with pytest.raises(IntegrityError, match="products_price_positive_chk"):
        repository.save(replace(product("TST-1"), price=Decimal("0")))


def test_stale_update_fails_with_optimistic_locking(repository: SqlProductRepository) -> None:
    # Two users load version 0 of the same product
    alice = repository.save(product("TST-1"))
    bob = replace(alice)

    repository.save(replace(bob, name="Bob's change"))  # version is now 1

    with pytest.raises(StaleDataError, match="changed concurrently"):
        repository.save(replace(alice, name="Alice's change, based on version 0"))


def test_update_of_a_missing_product_fails(repository: SqlProductRepository) -> None:
    with pytest.raises(StaleDataError, match="no longer exists"):
        repository.save(replace(product("TST-1"), id=999, version=0))
