"""Endpoint tests through TestClient.

Most use a fresh in-memory store (fast, isolated); the last one goes through the real
database (the Testcontainers PostgreSQL from conftest.py).
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ecommerce.main import app
from ecommerce.product.dependencies import get_product_service
from ecommerce.product.repository import InMemoryProductRepository
from ecommerce.product.service import ProductService

MUG = {"sku": "MUG-1", "name": "Mug", "price": "9.99"}


@pytest.fixture(autouse=True)
def fresh_store() -> Iterator[None]:
    """Swap the singleton store for an empty one (like @MockitoBean replacing a bean)."""
    service = ProductService(InMemoryProductRepository())
    app.dependency_overrides[get_product_service] = lambda: service
    yield
    app.dependency_overrides.clear()


def test_response_is_the_schema_with_camel_case_and_no_internal_fields(client: TestClient) -> None:
    created = client.post("/api/v1/products", json={**MUG, "categoryId": 3}).json()

    assert set(created) == {
        "id", "sku", "name", "description", "price", "status",
        "categoryId", "createdAt", "updatedAt",
    }  # fmt: skip
    assert created["categoryId"] == 3
    assert (created["description"], created["status"]) == ("", "ACTIVE")


def test_price_is_a_two_decimal_string(client: TestClient) -> None:
    created = client.post("/api/v1/products", json={**MUG, "price": "14.5"}).json()

    assert created["price"] == "14.50"


def test_create_ignores_fields_the_client_may_not_set(client: TestClient) -> None:
    created = client.post("/api/v1/products", json={**MUG, "id": 99, "version": 5}).json()

    assert created["id"] == 1  # assigned by the store, not taken from the request


def test_snake_case_is_accepted_too(client: TestClient) -> None:
    created = client.post("/api/v1/products", json={**MUG, "category_id": 4}).json()

    assert created["categoryId"] == 4


def test_list_is_empty_at_first(client: TestClient) -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    assert response.json() == {
        "items": [], "page": 0, "size": 20, "totalItems": 0, "totalPages": 0,
    }  # fmt: skip


def test_list_passes_page_and_size_and_reports_totals(client: TestClient) -> None:
    for n in range(1, 12):
        client.post("/api/v1/products", json={**MUG, "sku": f"MUG-{n}"})

    body = client.get("/api/v1/products", params={"page": 2, "size": 5}).json()

    assert (body["page"], body["size"], body["totalItems"], body["totalPages"]) == (2, 5, 11, 3)
    assert [p["sku"] for p in body["items"]] == ["MUG-11"]


def test_create_returns_201_with_location(client: TestClient) -> None:
    response = client.post("/api/v1/products", json=MUG)

    assert response.status_code == 201
    assert response.headers["Location"] == "/api/v1/products/1"
    assert response.json()["id"] == 1


def test_create_returns_409_on_duplicate_sku(client: TestClient) -> None:
    client.post("/api/v1/products", json=MUG)

    response = client.post("/api/v1/products", json=MUG)

    assert response.status_code == 409
    assert response.json()["code"] == "DUPLICATE_SKU"
    assert "MUG-1" in response.json()["message"]


def test_get_returns_product_and_404_when_missing(client: TestClient) -> None:
    client.post("/api/v1/products", json=MUG)

    assert client.get("/api/v1/products/1").json()["sku"] == "MUG-1"
    assert client.get("/api/v1/products/42").status_code == 404


def test_update_changes_fields(client: TestClient) -> None:
    client.post("/api/v1/products", json=MUG)

    response = client.put(
        "/api/v1/products/1",
        json={"name": "Big mug", "description": "", "price": "14.50", "status": "DISCONTINUED"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Big mug"
    assert response.json()["sku"] == "MUG-1"


def test_update_returns_404_when_missing(client: TestClient) -> None:
    response = client.put(
        "/api/v1/products/42",
        json={"name": "x", "description": "", "price": "1", "status": "ACTIVE"},
    )

    assert response.status_code == 404


def test_delete_is_a_soft_delete(client: TestClient) -> None:
    client.post("/api/v1/products", json=MUG)

    assert client.delete("/api/v1/products/1").status_code == 204
    # Still readable, now DISCONTINUED (SN-4)
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json()["status"] == "DISCONTINUED"


def test_delete_returns_404_when_missing(client: TestClient) -> None:
    assert client.delete("/api/v1/products/42").status_code == 404


@pytest.mark.usefixtures("clean_products")
def test_round_trip_through_the_database(client: TestClient) -> None:
    """The real providers: router -> service -> SqlProductRepository -> PostgreSQL."""
    app.dependency_overrides.clear()  # use the real database for this test

    created = client.post("/api/v1/products", json={**MUG, "sku": "INT-1", "price": "11.25"})
    assert created.status_code == 201
    product_id = created.json()["id"]

    listed = client.get("/api/v1/products").json()
    assert [(p["sku"], p["price"]) for p in listed["items"]] == [("INT-1", "11.25")]
    assert listed["totalItems"] == 1
    assert client.post("/api/v1/products", json={**MUG, "sku": "INT-1"}).status_code == 409

    assert client.delete(f"/api/v1/products/{product_id}").status_code == 204
    after = client.get(f"/api/v1/products/{product_id}").json()
    # Timestamps from the database are written in UTC with a Z suffix, like the Java app
    assert after["createdAt"].endswith("Z") and "+" not in after["createdAt"]
    assert after["status"] == "DISCONTINUED"
    assert "version" not in after  # internal field, not part of the API contract
