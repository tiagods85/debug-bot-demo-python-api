from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_items_first_page_returns_seeded_items() -> None:
    response = client.get("/api/items", params={"page": 1, "pageSize": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["items"][0]["name"] == "Widget A"
    assert body["items"][1]["name"] == "Widget B"


def test_create_item_with_valid_name_returns_created_item() -> None:
    response = client.post("/api/items", json={"name": "Widget D", "description": "a fresh item"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Widget D"
    assert body["description"] == "a fresh item"


def test_create_item_with_blank_name_is_rejected() -> None:
    response = client.post("/api/items", json={"name": "   ", "description": "should be rejected"})
    assert response.status_code == 422


def test_create_item_with_empty_name_is_rejected() -> None:
    response = client.post("/api/items", json={"name": "", "description": "should be rejected"})
    assert response.status_code == 422
