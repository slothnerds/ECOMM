"""Product storage: the contract (Protocol), the PostgreSQL implementation and an in-memory fake.

Products are never deleted, only discontinued (soft delete, spec rule SN-4).
"""

import itertools
import threading
from dataclasses import replace
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from ecommerce.product.models import Product, ProductStatus
from ecommerce.product.orm import ProductRow


class ProductRepository(Protocol):
    """Storage contract for products.

    A Protocol is structural: any class with these methods fits, no inheritance needed.
    """

    def save(self, product: Product) -> Product:
        """Insert when id is None (the database assigns it), otherwise update. Returns a copy."""
        ...

    def find_by_id(self, product_id: int) -> Product | None: ...

    def find_by_sku(self, sku: str) -> Product | None: ...

    def find_all(self) -> list[Product]:
        """All products, ordered by id."""
        ...

    def find_page(self, offset: int, limit: int) -> tuple[list[Product], int]:
        """Up to `limit` products after skipping `offset`, ordered by id, plus the total count."""
        ...


def _to_domain(row: ProductRow) -> Product:
    return Product(
        id=row.id,
        sku=row.sku,
        name=row.name,
        description=row.description,
        price=row.price,
        status=ProductStatus(row.status),
        category_id=row.category_id,
        version=row.version,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlProductRepository:
    """PostgreSQL implementation (the counterpart of JpaProductRepository.java).

    Uses the request's session from get_db(); each save is committed at once.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, product: Product) -> Product:
        if product.id is None:
            row = ProductRow(
                sku=product.sku,
                name=product.name,
                description=product.description,
                price=product.price,
                status=product.status.value,
                category_id=product.category_id,
            )
            self._session.add(row)
        else:
            found = self._session.get(ProductRow, product.id)
            if found is None:
                raise StaleDataError(f"Product {product.id} no longer exists")
            row = found
            # Optimistic locking: refuse to overwrite a newer version than the caller loaded
            if product.version is not None and product.version != row.version:
                raise StaleDataError(
                    f"Product {product.id} was changed concurrently "
                    f"(loaded version {product.version}, now {row.version})"
                )
            row.name = product.name
            row.description = product.description
            row.price = product.price
            row.status = product.status.value
            row.category_id = product.category_id
        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        self._session.refresh(row)  # read back database-generated values (id, timestamps)
        return _to_domain(row)

    def find_by_id(self, product_id: int) -> Product | None:
        row = self._session.get(ProductRow, product_id)
        return _to_domain(row) if row is not None else None

    def find_by_sku(self, sku: str) -> Product | None:
        row = self._session.scalars(select(ProductRow).where(ProductRow.sku == sku)).first()
        return _to_domain(row) if row is not None else None

    def find_all(self) -> list[Product]:
        return [
            _to_domain(row)
            for row in self._session.scalars(select(ProductRow).order_by(ProductRow.id))
        ]

    def find_page(self, offset: int, limit: int) -> tuple[list[Product], int]:
        """Two queries, like Spring Data: SELECT ... LIMIT/OFFSET and SELECT count(*)."""
        rows = self._session.scalars(
            select(ProductRow).order_by(ProductRow.id).offset(offset).limit(limit)
        )
        total = self._session.scalar(select(func.count()).select_from(ProductRow)) or 0
        return [_to_domain(row) for row in rows], total


class InMemoryProductRepository:
    """Thread-safe in-memory fake for fast service and router tests (the Stage 2 store).

    Stores and returns copies and keeps a version number, like the database does.
    """

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._ids = itertools.count(1)
        self._lock = threading.Lock()

    def save(self, product: Product) -> Product:
        with self._lock:
            stored = replace(product)
            if stored.id is None:
                stored.id = next(self._ids)
                stored.version = 0
            else:
                stored.version = (stored.version or 0) + 1
            self._products[stored.id] = stored
            return replace(stored)

    def find_by_id(self, product_id: int) -> Product | None:
        with self._lock:
            product = self._products.get(product_id)
            return replace(product) if product is not None else None

    def find_by_sku(self, sku: str) -> Product | None:
        with self._lock:
            match = next((p for p in self._products.values() if p.sku == sku), None)
            return replace(match) if match is not None else None

    def find_all(self) -> list[Product]:
        with self._lock:
            return [replace(p) for p in sorted(self._products.values(), key=lambda p: p.id or 0)]

    def find_page(self, offset: int, limit: int) -> tuple[list[Product], int]:
        everything = self.find_all()
        return everything[offset : offset + limit], len(everything)
