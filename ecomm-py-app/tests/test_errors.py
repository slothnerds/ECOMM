"""Validation (4.2) and the one error format (4.3) produced centrally (4.4).

The same cases as ErrorHandlingTest.java: both apps must return the same codes and messages.
"""

from collections.abc import Iterator
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from ecommerce.main import app
from ecommerce.product.dependencies import get_product_service
from ecommerce.product.exceptions import DuplicateSkuError, ProductNotFoundError
from ecommerce.product.service import ProductService

PRODUCTS = "/api/v1/products"


@pytest.fixture
def service() -> Iterator[Mock]:
    """A mock service (like @MockitoBean), so each test decides what it does."""
    mock = Mock(spec=ProductService)
    app.dependency_overrides[get_product_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


def fields(body: dict[str, Any]) -> list[tuple[str, str]]:
    return [(f["field"], f["message"]) for f in body["fieldErrors"]]


# ---------------------------------------------------------------- validation (400)


def test_missing_required_fields_are_listed_in_field_order(
    client: TestClient, service: Mock
) -> None:
    response = client.post(PRODUCTS, json={})
    body = response.json()

    assert response.status_code == 400
    assert body["code"] == "VALIDATION_FAILED"
    assert body["message"] == "Request validation failed"
    assert body["status"] == 400
    assert body["path"] == PRODUCTS
    assert body["timestamp"].endswith("Z")
    assert fields(body) == [
        ("name", "is required"),
        ("price", "is required"),
        ("sku", "is required"),
    ]
    service.create.assert_not_called()  # invalid input never reaches the service


def test_each_rule_has_its_own_message(client: TestClient, service: Mock) -> None:
    body = client.post(
        PRODUCTS, json={"sku": "bad", "name": "   ", "price": "-1", "categoryId": 0}
    ).json()

    assert fields(body) == [
        ("categoryId", "must be greater than 0"),
        ("name", "must not be blank"),
        ("price", "must be greater than 0"),
        ("sku", "must look like ABC-123 (3 capital letters, a dash, digits)"),
    ]


def test_length_and_money_precision_are_checked(client: TestClient, service: Mock) -> None:
    body = client.post(PRODUCTS, json={"sku": "ABC-1", "name": "x" * 201, "price": "12.345"}).json()

    assert fields(body) == [
        ("name", "must be at most 200 characters"),
        ("price", "must have at most 10 digits before and 2 after the decimal point"),
    ]


def test_wrong_type_is_a_field_error(client: TestClient, service: Mock) -> None:
    body = client.post(PRODUCTS, json={"sku": "ABC-1", "name": "Mug", "price": "abc"}).json()

    assert body["code"] == "VALIDATION_FAILED"
    assert fields(body) == [("price", "has an invalid value")]


def test_unknown_enum_value_lists_the_allowed_values(client: TestClient, service: Mock) -> None:
    body = client.put(
        f"{PRODUCTS}/1", json={"name": "Mug", "price": "9.99", "status": "SOLD_OUT"}
    ).json()

    assert fields(body) == [("status", "must be one of DRAFT, ACTIVE, DISCONTINUED")]


def test_update_requires_status(client: TestClient, service: Mock) -> None:
    body = client.put(f"{PRODUCTS}/1", json={"name": "Mug", "price": "9.99"}).json()

    assert fields(body) == [("status", "is required")]


def test_null_counts_as_missing(client: TestClient, service: Mock) -> None:
    body = client.post(PRODUCTS, json={"sku": "ABC-1", "name": None, "price": "9.99"}).json()

    assert fields(body) == [("name", "is required")]


def test_path_variable_of_wrong_type(client: TestClient, service: Mock) -> None:
    body = client.get(f"{PRODUCTS}/abc").json()

    assert body["code"] == "VALIDATION_FAILED"
    assert fields(body) == [("id", "has an invalid value")]


def test_page_and_size_are_validated(client: TestClient, service: Mock) -> None:
    both = client.get(PRODUCTS, params={"page": -1, "size": 101}).json()
    zero = client.get(PRODUCTS, params={"size": 0}).json()
    text = client.get(PRODUCTS, params={"page": "abc"}).json()

    assert both["code"] == "VALIDATION_FAILED"
    assert fields(both) == [
        ("page", "must be greater than or equal to 0"),
        ("size", "must be less than or equal to 100"),
    ]
    assert fields(zero) == [("size", "must be greater than or equal to 1")]
    assert fields(text) == [("page", "has an invalid value")]
    service.list.assert_not_called()


def test_broken_json_is_malformed(client: TestClient, service: Mock) -> None:
    response = client.post(
        PRODUCTS, content='{"sku": ', headers={"Content-Type": "application/json"}
    )
    body = response.json()

    assert response.status_code == 400
    assert body["code"] == "MALFORMED_REQUEST"
    assert body["message"] == "Request body is missing or is not valid JSON"
    assert body["fieldErrors"] == []


def test_missing_body_is_malformed(client: TestClient, service: Mock) -> None:
    response = client.post(PRODUCTS, headers={"Content-Type": "application/json"})

    assert (response.status_code, response.json()["code"]) == (400, "MALFORMED_REQUEST")


# ---------------------------------------------------------------- routing (404 / 405)


def test_unknown_url_is_not_found(client: TestClient) -> None:
    body = client.get("/api/v1/nope").json()

    assert (body["status"], body["code"]) == (404, "NOT_FOUND")
    assert body["message"] == "No endpoint GET /api/v1/nope"


def test_wrong_method_is_not_allowed(client: TestClient) -> None:
    body = client.patch(PRODUCTS).json()

    assert (body["status"], body["code"]) == (405, "METHOD_NOT_ALLOWED")
    assert body["message"] == "Method PATCH is not allowed for /api/v1/products"


# ---------------------------------------------------------------- business and data errors


def test_business_errors_carry_their_code(client: TestClient, service: Mock) -> None:
    service.get.side_effect = ProductNotFoundError(42)
    service.create.side_effect = DuplicateSkuError("ABC-1")

    not_found = client.get(f"{PRODUCTS}/42")
    duplicate = client.post(PRODUCTS, json={"sku": "ABC-1", "name": "Mug", "price": "9.99"})

    assert not_found.status_code == 404
    assert not_found.json()["code"] == "PRODUCT_NOT_FOUND"
    assert not_found.json()["message"] == "Product 42 not found"
    assert not_found.json()["path"] == f"{PRODUCTS}/42"
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == "DUPLICATE_SKU"
    assert duplicate.json()["message"] == "A product with SKU ABC-1 already exists"


def test_optimistic_lock_conflict_is_409(client: TestClient, service: Mock) -> None:
    service.update.side_effect = StaleDataError("version mismatch")

    response = client.put(
        f"{PRODUCTS}/1", json={"name": "Mug", "price": "9.99", "status": "ACTIVE"}
    )

    assert (response.status_code, response.json()["code"]) == (409, "CONCURRENT_UPDATE")


def test_database_constraint_is_409(client: TestClient, service: Mock) -> None:
    service.create.side_effect = IntegrityError("INSERT ...", {}, Exception("duplicate key"))

    response = client.post(PRODUCTS, json={"sku": "ABC-1", "name": "Mug", "price": "9.99"})

    assert (response.status_code, response.json()["code"]) == (409, "CONFLICT")


def test_unexpected_errors_hide_their_details(service: Mock) -> None:
    service.get.side_effect = RuntimeError("secret internal detail")

    # The error middleware re-raises after responding; tell TestClient not to re-raise it here
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get(f"{PRODUCTS}/1")

    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert response.json()["message"] == "An unexpected error occurred"
    assert "secret" not in response.text


def test_other_framework_http_errors_use_the_standard_body() -> None:
    """E.g. a library raising HTTPException(418): still the standard body, details not leaked."""
    from fastapi import FastAPI, HTTPException

    from ecommerce.core.errors import register_error_handlers

    other = FastAPI()
    register_error_handlers(other)

    @other.get("/teapot")
    def teapot() -> None:
        raise HTTPException(status_code=418, detail="internal detail")

    body = TestClient(other).get("/teapot").json()

    assert (body["code"], body["message"]) == ("INTERNAL_ERROR", "An unexpected error occurred")
