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


def test_list_is_empty_at_first(client: TestClient) -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    assert response.json() == []


def test_create_returns_201_with_location(client: TestClient) -> None:
    response = client.post("/api/v1/products", json=MUG)

    assert response.status_code == 201
    assert response.headers["Location"] == "/api/v1/products/1"
    assert response.json()["id"] == 1


def test_create_returns_409_on_duplicate_sku(client: TestClient) -> None:
    client.post("/api/v1/products", json=MUG)

    response = client.post("/api/v1/products", json=MUG)

    assert response.status_code == 409
    assert "MUG-1" in response.json()["detail"]


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
    assert [(p["sku"], p["price"]) for p in listed] == [("INT-1", "11.25")]
    assert client.post("/api/v1/products", json={**MUG, "sku": "INT-1"}).status_code == 409

    assert client.delete(f"/api/v1/products/{product_id}").status_code == 204
    after = client.get(f"/api/v1/products/{product_id}").json()
    assert (after["status"], after["version"]) == ("DISCONTINUED", 1)
