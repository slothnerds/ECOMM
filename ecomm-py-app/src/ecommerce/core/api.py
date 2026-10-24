"""Building blocks shared by every API model: JSON conventions and validated field types.

The counterpart of the Java app's DTO conventions and core/error/ValidationMessages.java; the
messages must stay identical to the Java ones, so both apps return the same field errors.
"""

import re
from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, PlainSerializer
from pydantic.alias_generators import to_camel


class Messages:
    """Field error texts, identical to ValidationMessages.java."""

    REQUIRED = "is required"
    NOT_BLANK = "must not be blank"
    GREATER_THAN_0 = "must be greater than 0"
    MONEY_DIGITS = "must have at most 10 digits before and 2 after the decimal point"
    SKU_FORMAT = "must look like ABC-123 (3 capital letters, a dash, digits)"
    INVALID_VALUE = "has an invalid value"


class ApiModel(BaseModel):
    """Common settings: camelCase JSON (categoryId), like the Java app; snake_case also accepted."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# ---------------------------------------------------------------------------------------------
# Output types
# ---------------------------------------------------------------------------------------------


def _utc_iso(value: datetime) -> str:
    """2026-10-21T12:14:00Z: converted to UTC, with Z instead of +00:00 (like Java's Instant)."""
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


# A datetime that is always written to JSON in UTC with a Z suffix
UtcDateTime = Annotated[datetime, PlainSerializer(_utc_iso, return_type=str)]


def _money(value: Decimal) -> str:
    """Always 2 decimals ("14.50"), also when a client sent "14.5"; the column is numeric(12,2)."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# A Decimal amount that is always written to JSON as a string with 2 decimals
Money = Annotated[Decimal, PlainSerializer(_money, return_type=str)]


# ---------------------------------------------------------------------------------------------
# Validated input types (the counterpart of the Bean Validation annotations on the Java DTOs)
# ---------------------------------------------------------------------------------------------


def _not_blank(value: str) -> str:
    if not value.strip():
        raise ValueError(Messages.NOT_BLANK)
    return value


_SKU = re.compile(r"[A-Z]{3}-\d{1,28}")


def _sku_format(value: str) -> str:
    if not _SKU.fullmatch(value):
        raise ValueError(Messages.SKU_FORMAT)
    return value


# Required text, 1-200 characters, not only spaces (Java: @NotNull @Pattern @Size(max = 200))
Name = Annotated[str, Field(max_length=200), AfterValidator(_not_blank)]

# ABC-123: 3 capital letters, a dash, 1-28 digits (Java: @Pattern(regexp = SKU_PATTERN))
Sku = Annotated[str, AfterValidator(_sku_format)]

# Optional long text (Java: @Size(max = 2000))
Description = Annotated[str | None, Field(max_length=2000)]

# > 0 with at most 10 + 2 digits, fits numeric(12,2) (Java: @DecimalMin(exclusive 0) @Digits(10, 2))
Price = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]

# Optional id, > 0 (Java: @Positive)
PositiveId = Annotated[int | None, Field(gt=0)]
