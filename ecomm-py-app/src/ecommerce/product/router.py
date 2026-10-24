"""Product CRUD endpoints (the counterpart of ProductController.java).

Requests and responses are the Pydantic schemas in product/schemas.py; the Product dataclass
never leaves the service. Errors are not handled here: the service raises, and the central
handlers in core/errors.py turn every exception into the standard error body.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from ecommerce.core.paging import PageResponse
from ecommerce.product.dependencies import get_product_service
from ecommerce.product.schemas import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from ecommerce.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["products"])

# Annotated bundles the type and how to get it, so each endpoint signature stays short
Service = Annotated[ProductService, Depends(get_product_service)]
# The URL segment is called "id" (as in the Java app, and in error messages); the Python
# parameter is product_id so it doesn't shadow the built-in id()
ProductId = Annotated[int, Path(alias="id")]


@router.get("")
def list_products(
    service: Service,
    page: Annotated[int, Query(ge=0)] = 0,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PageResponse[ProductResponse]:
    """One page of products, ordered by id: ?page=0&size=20 (out-of-range values -> 400)."""
    return PageResponse[ProductResponse].of(
        service.list(page, size), ProductResponse.model_validate
    )


@router.get("/{id}")
def get_product(product_id: ProductId, service: Service) -> ProductResponse:
    return ProductResponse.model_validate(service.get(product_id))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductCreateRequest, response: Response, service: Service
) -> ProductResponse:
    """201 Created with a Location header pointing at the new product."""
    created = service.create(request.to_product())
    response.headers["Location"] = f"/api/v1/products/{created.id}"
    return ProductResponse.model_validate(created)


@router.put("/{id}")
def update_product(
    product_id: ProductId, request: ProductUpdateRequest, service: Service
) -> ProductResponse:
    return ProductResponse.model_validate(service.update(product_id, request.to_update()))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: ProductId, service: Service) -> None:
    """Soft delete: the product becomes DISCONTINUED (204 No Content)."""
    service.delete(product_id)
