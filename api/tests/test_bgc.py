import aiohttp
import pytest
from aioresponses import aioresponses
from api.bgc import login, load_game_state

@pytest.fixture
def bgc_api():
    with aioresponses() as api:
        yield api

@pytest.fixture
async def session():
    async with aiohttp.ClientSession('http://play.boardgamecore.net') as session:
        yield session

async def test_login(session, bgc_api):
    bgc_api.post('/login.jsp', status=200, body='ok')
    await login(session, 'user', 'pass')
    bgc_api.assert_called_once_with('/login.jsp', data={'login':'user', 'password':'pass'}, method='POST')

async def test_load_game_state(session, bgc_api):
    bgc_api.post('/Json', status=200, body='[]')
    data = await load_game_state(session, 123)
    assert data == '[]'
    bgc_api.assert_called_once_with('/Json', data={'id': 123, 'action':'initLoad'}, method='POST')

