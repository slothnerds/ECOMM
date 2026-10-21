"""Request and response shapes of the product API (the counterpart of product/web/dto in Java).

Endpoints accept and return only these Pydantic models; the Product dataclass and the
ProductRow ORM class never leave the service and repository layers.
"""

from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer
from pydantic.alias_generators import to_camel

from ecommerce.product.models import Product, ProductStatus, ProductUpdate


def _utc_iso(value: datetime) -> str:
    """2026-10-21T12:14:00Z: converted to UTC, with Z instead of +00:00 (like Java's Instant)."""
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


# A datetime that is always written to JSON in UTC with a Z suffix
UtcDateTime = Annotated[datetime, PlainSerializer(_utc_iso, return_type=str)]


def _money(value: Decimal) -> str:
    """Always 2 decimals ("14.50"), also when a client sent "14.5"; the column is numeric(12,2)."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# A Decimal amount that is always written to JSON as a string with 2 decimals
Money = Annotated[Decimal, PlainSerializer(_money, return_type=str)]


class ApiModel(BaseModel):
    """Common settings: camelCase JSON (categoryId), like the Java app; snake_case also accepted."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ProductCreateRequest(ApiModel):
    """Body of POST /api/v1/products: only what a client may set.

    Anything else in the JSON (id, version, timestamps) is ignored, so it can't reach the
    domain object.
    """

    sku: str
    name: str
    description: str = ""
    price: Decimal
    # DRAFT creates a product that isn't for sale yet
    status: ProductStatus = ProductStatus.ACTIVE
    category_id: int | None = None

    def to_product(self) -> Product:
        """A new, unsaved product; the database assigns id, version and timestamps."""
        return Product(
            sku=self.sku,
            name=self.name,
            description=self.description,
            price=self.price,
            status=self.status,
            category_id=self.category_id,
        )


class ProductUpdateRequest(ApiModel):
    """Body of PUT /api/v1/products/{id}. The SKU is not here: it can't change after creation."""

    name: str
    description: str = ""
    price: Decimal
    status: ProductStatus

    def to_update(self) -> ProductUpdate:
        """The service's input; keeps HTTP models out of the service layer."""
        return ProductUpdate(
            name=self.name, description=self.description, price=self.price, status=self.status
        )


class ProductResponse(ApiModel):
    """What the API returns for a product: the public contract, independent of storage.

    Internal fields such as the optimistic-locking version are deliberately left out.
    Formats (same in the Java app): price is a string with 2 decimals ("89.90"; Pydantic writes
    Decimal as text), timestamps are UTC with a Z suffix.
    """

    # Read the values from a Product object's attributes (ProductResponse.model_validate(product))
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    description: str
    price: Money
    status: ProductStatus
    category_id: int | None
    created_at: UtcDateTime | None
    updated_at: UtcDateTime | None
