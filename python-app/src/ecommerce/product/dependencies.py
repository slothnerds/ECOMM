"""Dependency providers: FastAPI's counterpart of Spring wiring beans together.

Depends() calls these functions on every request: each request gets its own database session
(from get_db), wrapped in a repository and a service. They are cheap to create; the shared,
long-lived part is the engine's connection pool.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ecommerce.core.db import get_db
from ecommerce.product.repository import ProductRepository, SqlProductRepository
from ecommerce.product.service import ProductService


def get_product_repository(session: Annotated[Session, Depends(get_db)]) -> ProductRepository:
    return SqlProductRepository(session)


def get_product_service(
    repository: Annotated[ProductRepository, Depends(get_product_repository)],
) -> ProductService:
    return ProductService(repository)
