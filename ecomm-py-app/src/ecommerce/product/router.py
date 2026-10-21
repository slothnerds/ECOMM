"""Product CRUD endpoints (the counterpart of ProductController.java).

Requests and responses are the Pydantic schemas in product/schemas.py; the Product dataclass
never leaves the service. Stage 4 replaces the try/except blocks with central error handling.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ecommerce.product.dependencies import get_product_service
from ecommerce.product.exceptions import DuplicateSkuError, ProductNotFoundError
from ecommerce.product.schemas import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from ecommerce.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["products"])

# Annotated bundles the type and how to get it, so each endpoint signature stays short
Service = Annotated[ProductService, Depends(get_product_service)]


@router.get("")
def list_products(service: Service) -> list[ProductResponse]:
    return [ProductResponse.model_validate(product) for product in service.list()]


@router.get("/{product_id}")
def get_product(product_id: int, service: Service) -> ProductResponse:
    try:
        return ProductResponse.model_validate(service.get(product_id))
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductCreateRequest, response: Response, service: Service
) -> ProductResponse:
    """201 Created with a Location header pointing at the new product."""
    try:
        created = service.create(request.to_product())
    except DuplicateSkuError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    response.headers["Location"] = f"/api/v1/products/{created.id}"
    return ProductResponse.model_validate(created)


@router.put("/{product_id}")
def update_product(
    product_id: int, request: ProductUpdateRequest, service: Service
) -> ProductResponse:
    try:
        return ProductResponse.model_validate(service.update(product_id, request.to_update()))
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: Service) -> None:
    """Soft delete: the product becomes DISCONTINUED (204 No Content)."""
    try:
        service.delete(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
