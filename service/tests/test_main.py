import pytest
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

from ..core.config import RESPONSE_TEMPLATE, WORDS_URL
from ..main import app


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["my_local_test_host"]


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://my_local_test_host") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert 'docs' in response.text
    assert 'madlib' in response.text


@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url="http://my_local_test_host") as ac:
        response = await ac.get("ping")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_madlib(httpx_mock: HTTPXMock):
    words = {
        'adjective': 'nice',
        'verb': 'improve',
        'noun': 'vegetable'
    }
    for word in words:
        httpx_mock.add_response(url=f'{WORDS_URL}{word}', json=words[f'{word}'])

    async with AsyncClient(app=app, base_url="http://my_local_test_host") as async_client:
        response = await async_client.get("madlib")

    assert response.status_code == 200
    assert response.json() == RESPONSE_TEMPLATE.format(**words)
    assert len(httpx_mock.get_requests()) == 3
