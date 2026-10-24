"""Business rules for the catalog (the counterpart of ProductService.java)."""

from dataclasses import replace

from ecommerce.core.paging import Page
from ecommerce.product.exceptions import DuplicateSkuError, ProductNotFoundError
from ecommerce.product.models import Product, ProductStatus, ProductUpdate
from ecommerce.product.repository import ProductRepository


class ProductService:
    """Endpoints call this; only this calls the repository."""

    def __init__(self, repository: ProductRepository) -> None:
        # Explicit constructor injection: whoever creates the service passes the repository
        self._repository = repository

    def create(self, product: Product) -> Product:
        """Create a product; the SKU must be unique.

        Fields the database manages (id, version, timestamps) are ignored if the caller sent them.
        """
        if self._repository.find_by_sku(product.sku) is not None:
            raise DuplicateSkuError(product.sku)
        return self._repository.save(
            replace(product, id=None, version=None, created_at=None, updated_at=None)
        )

    def get(self, product_id: int) -> Product:
        product = self._repository.find_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def list(self, page: int, size: int) -> Page[Product]:
        """One page of the catalog, ordered by id so pages are stable.

        Page numbers start at 0; a page past the end is empty. The router validates page and size.
        """
        items, total = self._repository.find_page(offset=page * size, limit=size)
        return Page(items=items, page=page, size=size, total_items=total)

    def update(self, product_id: int, update: ProductUpdate) -> Product:
        """Change name, description, price and status. The SKU never changes."""
        product = self.get(product_id)
        product.name = update.name
        product.description = update.description
        product.price = update.price
        product.status = update.status
        return self._repository.save(product)

    def delete(self, product_id: int) -> None:
        """Soft delete (spec rule SN-4): the product becomes DISCONTINUED instead of being removed,
        because carts and orders reference it. It stays readable by id.
        """
        product = self.get(product_id)
        product.status = ProductStatus.DISCONTINUED
        self._repository.save(product)
