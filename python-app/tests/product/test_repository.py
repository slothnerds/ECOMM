"""Tests of the in-memory fake (used by the service and router tests); the PostgreSQL
repository is tested in test_sql_repository.py.
"""

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest

from ecommerce.product.models import Product
from ecommerce.product.repository import InMemoryProductRepository, ProductRepository


@pytest.fixture
def repository() -> ProductRepository:
    """A fresh, empty store for every test (pytest fixtures are function-scoped by default)."""
    return InMemoryProductRepository()


def product(sku: str) -> Product:
    return Product(sku=sku, name=f"Product {sku}", price=Decimal("9.99"))


def test_save_assigns_sequential_ids(repository: ProductRepository) -> None:
    assert repository.save(product("A-1")).id == 1
    assert repository.save(product("A-2")).id == 2


def test_find_by_id_and_sku(repository: ProductRepository) -> None:
    saved = repository.save(product("A-1"))
    assert saved.id is not None

    assert repository.find_by_id(saved.id) == saved
    assert repository.find_by_sku("A-1") == saved
    assert repository.find_by_id(999) is None
    assert repository.find_by_sku("NOPE-1") is None


def test_save_with_existing_id_replaces(repository: ProductRepository) -> None:
    saved = repository.save(product("A-1"))
    assert saved.id is not None
    saved.price = Decimal("12.00")

    repository.save(saved)

    assert len(repository.find_all()) == 1
    found = repository.find_by_id(saved.id)
    assert found is not None
    assert found.price == Decimal("12.00")


def test_find_all_is_ordered_by_id(repository: ProductRepository) -> None:
    for sku in ("A-1", "A-2", "A-3"):
        repository.save(product(sku))

    assert [p.sku for p in repository.find_all()] == ["A-1", "A-2", "A-3"]


def test_version_starts_at_0_and_increments_on_update(repository: ProductRepository) -> None:
    saved = repository.save(product("A-1"))
    assert saved.version == 0

    assert repository.save(saved).version == 1


def test_returned_products_are_copies(repository: ProductRepository) -> None:
    saved = repository.save(product("A-1"))
    assert saved.id is not None

    saved.name = "changed without saving"

    found = repository.find_by_id(saved.id)
    assert found is not None
    assert found.name == "Product A-1"


def test_parallel_saves_get_unique_ids(repository: ProductRepository) -> None:
    with ThreadPoolExecutor(max_workers=16) as pool:
        list(pool.map(lambda i: repository.save(product(f"P-{i}")), range(100)))

    ids = [p.id for p in repository.find_all()]
    assert len(ids) == 100
    assert len(set(ids)) == 100
