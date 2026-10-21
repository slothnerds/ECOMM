"""Product domain model (the counterpart of Product.java).

Plain dataclasses with no database code; product/orm.py maps them to table ecomm.products.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class ProductStatus(StrEnum):
    """Lifecycle of a catalog product; stored as text, matching products_status_chk."""

    DRAFT = "DRAFT"  # being prepared; not visible to customers yet
    ACTIVE = "ACTIVE"  # for sale
    DISCONTINUED = "DISCONTINUED"  # no longer sold, kept because orders reference it (SN-4)


@dataclass(slots=True, eq=False)
class Product:
    """A catalog product.

    Equality is by ``id`` only (entity identity), matching the Java version.
    """

    sku: str
    name: str
    # Exact decimal amount; never use float for money (spec rule SN-3)
    price: Decimal
    description: str = ""
    status: ProductStatus = ProductStatus.ACTIVE
    # The Category model comes with categories in Stage 5
    category_id: int | None = None
    # Managed by the database / repository; None until saved
    id: int | None = None
    version: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Product):
            return NotImplemented
        # Unsaved products (id None) are only equal to themselves
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        # Constant per class, so the hash doesn't change when the id is assigned on save
        return hash(Product)


@dataclass(frozen=True, slots=True)
class ProductUpdate:
    """The fields an update may change.

    Id and SKU are deliberately absent: the SKU is fixed after creation because
    orders reference it.
    """

    name: str
    description: str
    price: Decimal
    status: ProductStatus
