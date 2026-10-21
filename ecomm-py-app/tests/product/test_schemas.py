from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal

from ecommerce.product.models import Product
from ecommerce.product.schemas import ProductResponse

CHICAGO = timezone(timedelta(hours=-5))


def test_timestamps_are_converted_to_utc_with_z() -> None:
    product = Product(
        id=1,
        sku="MUG-1",
        name="Mug",
        price=Decimal("9.99"),
        created_at=datetime(2026, 10, 21, 7, 14, tzinfo=CHICAGO),
        updated_at=datetime(2026, 10, 21, 12, 0, 0, 123456, tzinfo=UTC),
    )

    body = ProductResponse.model_validate(product).model_dump(mode="json", by_alias=True)

    assert body["createdAt"] == "2026-10-21T12:14:00Z"  # 07:14 at -05:00 is 12:14 UTC
    assert body["updatedAt"] == "2026-10-21T12:00:00.123456Z"


def test_price_is_a_two_decimal_string() -> None:
    product = Product(id=1, sku="MUG-1", name="Mug", price=Decimal("14.5"))

    body = ProductResponse.model_validate(product).model_dump(mode="json", by_alias=True)

    assert body["price"] == "14.50"
    assert body["createdAt"] is None  # unsaved objects have no timestamps
