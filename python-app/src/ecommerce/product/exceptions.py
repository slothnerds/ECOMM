"""Product domain errors. They are mapped to HTTP responses in Stage 4."""


class ProductNotFoundError(Exception):
    """No product exists with the requested id (404)."""

    def __init__(self, product_id: int) -> None:
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id


class DuplicateSkuError(Exception):
    """Another product already uses this SKU (409)."""

    def __init__(self, sku: str) -> None:
        super().__init__(f"A product with SKU {sku} already exists")
        self.sku = sku
