"""Product domain errors. The central handlers in core/errors.py turn them into responses."""

from ecommerce.core.errors import BusinessError, ErrorCode


class ProductNotFoundError(BusinessError):
    """No product exists with the requested id (404 PRODUCT_NOT_FOUND)."""

    code = ErrorCode.PRODUCT_NOT_FOUND

    def __init__(self, product_id: int) -> None:
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id


class DuplicateSkuError(BusinessError):
    """Another product already uses this SKU (409 DUPLICATE_SKU)."""

    code = ErrorCode.DUPLICATE_SKU

    def __init__(self, sku: str) -> None:
        super().__init__(f"A product with SKU {sku} already exists")
        self.sku = sku
