"""SQLAlchemy mapping of table ecomm.products (counterpart of the JPA annotations in Product.java).

Kept separate from the Product dataclass: the domain model stays free of database code, and
slots=True dataclasses can't be instrumented by SQLAlchemy anyway.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, Identity, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce.core.db import Base


class ProductRow(Base):
    __tablename__ = "products"

    # GENERATED ALWAYS AS IDENTITY: the database assigns it
    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    category_id: Mapped[int | None] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    version: Mapped[int] = mapped_column(BigInteger)

    __mapper_args__ = {
        # Optimistic locking: UPDATE ... WHERE version = <loaded version>, then version + 1.
        # Start at 0 like the table default and Hibernate (SQLAlchemy's default starts at 1).
        "version_id_col": version,
        "version_id_generator": lambda current: 0 if current is None else current + 1,
    }
