import aiohttp
import pytest
from aioresponses import aioresponses
from api.bgc import login

@pytest.fixture
def bgc_api():
    with aioresponses() as api:
        yield api

@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session

async def test_login(session, bgc_api):
    bgc_api.post('http://play.boardgamecore.net/login.jsp', status=200, body='ok')
    await login(session, 'user', 'pass')
    bgc_api.assert_called_once_with('http://play.boardgamecore.net/login.jsp', data={'login':'user', 'password':'pass'}, method='POST')
