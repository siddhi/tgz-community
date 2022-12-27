import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from aiohttp import ClientSession
from . import bgc
import json
import os

templates = Jinja2Templates(directory='templates')

BGC_USERNAME = os.environ['BGC_USERNAME']
BGC_PASSWORD = os.environ['BGC_PASSWORD']
GAME_IDS = [100509, 100497]

async def process_game(session, id):
    data = await bgc.load_game_state(session, id)
    return json.loads(data)

async def homepage(request):
    async with ClientSession('http://play.boardgamecore.net') as session:
        await bgc.login(session, BGC_USERNAME, BGC_PASSWORD)
        data = await asyncio.gather(*[process_game(session, id) for id in GAME_IDS])
        return templates.TemplateResponse('dashboard.html', {'request': request, 'games': data})

app = Starlette(routes=[
    Route('/', homepage)
])
