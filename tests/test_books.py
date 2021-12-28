import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_books(test_app: AsyncClient) -> None:
    response = await test_app.get("/api/v1/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_post_book(test_app: AsyncClient) -> None:
    data = {"title": "Test book", "author": "Author"}
    response = await test_app.post("/api/v1/books/", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test book"
    assert response.json()["author"] == "Author"


@pytest.mark.asyncio
async def test_put_book_async(test_app: AsyncClient) -> None:
    data = {"title": "Test book UPD"}
    response = await test_app.put("/api/v1/books/1", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["title"] == "Test book UPD"
    assert response.json()["title"] != "Test book"
    assert response.json()["author"] == "Author"


@pytest.mark.asyncio
async def test_get_book_by_id_async(test_app: AsyncClient) -> None:
    response = await test_app.get("/api/v1/books/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unallowed_method_book_async(test_app: AsyncClient) -> None:
    response = await test_app.delete("/api/v1/books/")
    assert response.status_code == 405


@pytest.mark.asyncio
async def test_delete_book_async(test_app: AsyncClient) -> None:
    response = await test_app.delete("/api/v1/books/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_delete_book_invalid_id_async(test_app: AsyncClient) -> None:
    response = await test_app.delete("/api/v1/books/999999")
    assert response.status_code == 404
