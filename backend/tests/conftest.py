import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture(scope="session")
async def test_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
