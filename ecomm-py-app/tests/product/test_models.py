from decimal import Decimal

import pytest

from ecommerce.product.models import Product, ProductStatus


def test_defaults_to_active_status_and_unsaved() -> None:
    product = Product(sku="ABC-1", name="Mug", price=Decimal("12.50"))

    assert product.name == "Mug"
    assert product.id is None
    assert product.status is ProductStatus.ACTIVE
    assert product.version is None


def test_float_is_inexact_but_decimal_is_exact() -> None:
    assert 0.1 + 0.2 != 0.3  # 0.30000000000000004
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")


def test_decimal_from_float_carries_the_error() -> None:
    # Always build money from a str, never from a float
    assert Decimal(0.1) != Decimal("0.1")


def test_products_with_same_id_are_equal_even_if_fields_differ() -> None:
    a = Product(id=1, sku="ABC-1", name="Mug", price=Decimal("10.00"))
    b = Product(id=1, sku="ABC-1", name="Mug v2", price=Decimal("12.00"))

    assert a == b
    assert hash(a) == hash(b)


def test_unsaved_products_are_only_equal_to_themselves() -> None:
    a = Product(sku="ABC-1", name="A", price=Decimal("1.00"))
    b = Product(sku="ABC-1", name="A", price=Decimal("1.00"))

    assert a == a
    assert a != b


def test_product_is_never_equal_to_another_type() -> None:
    product = Product(id=1, sku="ABC-1", name="Mug", price=Decimal("1.00"))

    # __eq__ returns NotImplemented, so Python tries the other side, then falls back to False
    assert product != "ABC-1"
    assert product != 1


def test_product_stays_findable_in_set_after_id_is_assigned() -> None:
    product = Product(sku="ABC-1", name="Mug", price=Decimal("1.00"))
    products = {product}

    product.id = 42  # what saving to the database will do

    assert product in products


def test_slots_reject_unknown_attributes() -> None:
    product = Product(sku="ABC-1", name="Mug", price=Decimal("1.00"))

    # mypy already flags this typo statically; slots=True also rejects it at runtime
    with pytest.raises(AttributeError):
        product.prise = Decimal("2.00")  # type: ignore[attr-defined]  # deliberate typo
