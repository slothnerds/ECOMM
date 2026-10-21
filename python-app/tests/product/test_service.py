"""Service tests, mostly with a real in-memory repository (a "fake").

Fakes check outcomes ("the store now has one product"). The last test shows the
Mockito style with unittest.mock, which checks interactions ("save was never called").
"""

from dataclasses import replace
from decimal import Decimal
from unittest.mock import Mock

import pytest

from ecommerce.product.exceptions import DuplicateSkuError, ProductNotFoundError
from ecommerce.product.models import Product, ProductStatus, ProductUpdate
from ecommerce.product.repository import InMemoryProductRepository, ProductRepository
from ecommerce.product.service import ProductService


@pytest.fixture
def repository() -> InMemoryProductRepository:
    return InMemoryProductRepository()


@pytest.fixture
def service(repository: InMemoryProductRepository) -> ProductService:
    # Fixtures can use other fixtures: pytest passes the same repository to both
    return ProductService(repository)


def mug(product_id: int | None = None) -> Product:
    return Product(id=product_id, sku="MUG-1", name="Mug", price=Decimal("9.99"))


def test_create_assigns_an_id(service: ProductService) -> None:
    created = service.create(mug())

    assert created.id == 1
    assert service.list() == [created]


def test_create_ignores_an_id_on_the_input(service: ProductService) -> None:
    created = service.create(mug(product_id=99))

    assert created.id == 1


def test_create_rejects_duplicate_sku(
    service: ProductService, repository: InMemoryProductRepository
) -> None:
    service.create(mug())

    with pytest.raises(DuplicateSkuError, match="MUG-1"):
        service.create(mug())
    assert len(repository.find_all()) == 1


def test_get_raises_when_missing(service: ProductService) -> None:
    with pytest.raises(ProductNotFoundError, match="Product 42 not found"):
        service.get(42)


def test_update_changes_fields_but_keeps_sku(service: ProductService) -> None:
    created = service.create(mug())
    assert created.id is not None

    updated = service.update(
        created.id, ProductUpdate("Big mug", "500 ml", Decimal("14.50"), ProductStatus.DISCONTINUED)
    )

    assert updated.name == "Big mug"
    assert updated.price == Decimal("14.50")
    assert updated.status is ProductStatus.DISCONTINUED
    assert updated.sku == "MUG-1"
    assert service.get(created.id).name == "Big mug"  # persisted, not just returned


def test_update_raises_when_missing(service: ProductService) -> None:
    with pytest.raises(ProductNotFoundError):
        service.update(42, ProductUpdate("x", "", Decimal("1"), ProductStatus.ACTIVE))


def test_delete_is_a_soft_delete(service: ProductService) -> None:
    created = service.create(mug())
    assert created.id is not None

    service.delete(created.id)

    # Still readable by id, now DISCONTINUED (SN-4)
    assert service.get(created.id).status is ProductStatus.DISCONTINUED


def test_create_resets_database_managed_fields(service: ProductService) -> None:
    created = service.create(replace(mug(product_id=99), version=7))

    assert created.id == 1
    assert created.version == 0


def test_delete_raises_when_missing(service: ProductService) -> None:
    with pytest.raises(ProductNotFoundError):
        service.delete(42)


def test_duplicate_sku_never_calls_save_mock_style() -> None:
    # spec= makes the mock reject methods ProductRepository doesn't have
    repository = Mock(spec=ProductRepository)
    repository.find_by_sku.return_value = mug(product_id=1)  # like Mockito's when(...).thenReturn
    service = ProductService(repository)

    with pytest.raises(DuplicateSkuError):
        service.create(mug())

    repository.find_by_sku.assert_called_once_with("MUG-1")  # like verify(repository)
    repository.save.assert_not_called()  # like verify(repository, never()).save(any())
