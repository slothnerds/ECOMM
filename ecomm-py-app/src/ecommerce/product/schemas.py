"""Request and response shapes of the product API (the counterpart of product/web/dto in Java).

Endpoints accept and return only these Pydantic models; the Product dataclass and the
ProductRow ORM class never leave the service and repository layers. Requests are validated
by the field types from core/api.py (the counterpart of the Bean Validation annotations).
"""

from pydantic import ConfigDict

from ecommerce.core.api import (
    ApiModel,
    Description,
    Money,
    Name,
    PositiveId,
    Price,
    Sku,
    UtcDateTime,
)
from ecommerce.product.models import Product, ProductStatus, ProductUpdate


class ProductCreateRequest(ApiModel):
    """Body of POST /api/v1/products: only what a client may set.

    Anything else in the JSON (id, version, timestamps) is ignored, so it can't reach the
    domain object.
    """

    sku: Sku
    name: Name
    description: Description = None
    price: Price
    # Optional; DRAFT creates a product that isn't for sale yet, default ACTIVE
    status: ProductStatus | None = None
    category_id: PositiveId = None

    def to_product(self) -> Product:
        """A new, unsaved product; the database assigns id, version and timestamps."""
        return Product(
            sku=self.sku,
            name=self.name,
            description=self.description or "",
            price=self.price,
            status=self.status or ProductStatus.ACTIVE,
            category_id=self.category_id,
        )


class ProductUpdateRequest(ApiModel):
    """Body of PUT /api/v1/products/{id}. The SKU is not here: it can't change after creation."""

    name: Name
    description: Description = None
    price: Price
    status: ProductStatus

    def to_update(self) -> ProductUpdate:
        """The service's input; keeps HTTP models out of the service layer."""
        return ProductUpdate(
            name=self.name,
            description=self.description or "",
            price=self.price,
            status=self.status,
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
