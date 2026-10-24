"""Paging: the Page returned by services, and the PageResponse sent as JSON.

The counterpart of Spring Data's Page (service side) and core/web/PageResponse.java (API side).
"""

from collections.abc import Callable
from dataclasses import dataclass

from ecommerce.core.api import ApiModel


@dataclass(frozen=True, slots=True)
class Page[T]:
    """One page of results plus the numbers needed to page through all of them."""

    items: list[T]
    page: int  # 0-based
    size: int
    total_items: int

    @property
    def total_pages(self) -> int:
        """Pages needed for all items (0 when there are none), rounding up."""
        return -(-self.total_items // self.size)


class PageResponse[T](ApiModel):
    """One page of results as JSON, the same shape as the Java app's PageResponse."""

    items: list[T]
    page: int
    size: int
    total_items: int
    total_pages: int

    @classmethod
    def of[E](cls, page: Page[E], mapper: Callable[[E], T]) -> PageResponse[T]:
        """Converts a service Page, mapping each item to its response model."""
        return cls(
            items=[mapper(item) for item in page.items],
            page=page.page,
            size=page.size,
            total_items=page.total_items,
            total_pages=page.total_pages,
        )
