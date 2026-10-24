from ecommerce.core.paging import Page, PageResponse


def test_total_pages_rounds_up_and_is_zero_without_items() -> None:
    assert Page(items=[], page=0, size=5, total_items=11).total_pages == 3
    assert Page(items=[], page=0, size=5, total_items=10).total_pages == 2
    assert Page(items=[], page=0, size=5, total_items=0).total_pages == 0


def test_page_response_maps_items_and_uses_camel_case() -> None:
    page = Page(items=[1, 2], page=1, size=2, total_items=5)

    body = PageResponse[str].of(page, str).model_dump(by_alias=True)

    assert body == {"items": ["1", "2"], "page": 1, "size": 2, "totalItems": 5, "totalPages": 3}
