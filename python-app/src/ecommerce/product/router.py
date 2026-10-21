"""Product CRUD endpoints (the counterpart of ProductController.java).

Stage 2 exposes the model dataclasses directly; Stage 4 introduces request/response
schemas and central error handling (replacing the try/except blocks below).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ecommerce.product.dependencies import get_product_service
from ecommerce.product.exceptions import DuplicateSkuError, ProductNotFoundError
from ecommerce.product.models import Product, ProductUpdate
from ecommerce.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["products"])

# Annotated bundles the type and how to get it, so each endpoint signature stays short
Service = Annotated[ProductService, Depends(get_product_service)]


@router.get("")
def list_products(service: Service) -> list[Product]:
    return service.list()


@router.get("/{product_id}")
def get_product(product_id: int, service: Service) -> Product:
    try:
        return service.get(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(product: Product, response: Response, service: Service) -> Product:
    """201 Created with a Location header pointing at the new product."""
    try:
        created = service.create(product)
    except DuplicateSkuError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    response.headers["Location"] = f"/api/v1/products/{created.id}"
    return created


@router.put("/{product_id}")
def update_product(product_id: int, update: ProductUpdate, service: Service) -> Product:
    try:
        return service.update(product_id, update)
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: Service) -> None:
    """Soft delete: the product becomes DISCONTINUED (204 No Content)."""
    try:
        service.delete(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
