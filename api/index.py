import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from aiohttp import ClientSession
from . import bgc, model, filters
import json
import os

templates = Jinja2Templates(directory='templates')
templates.env.filters['humanise'] = filters.humanise
templates.env.filters['underscore_to_space'] = filters.underscore_to_space

BGC_USERNAME = os.environ['BGC_USERNAME']
BGC_PASSWORD = os.environ['BGC_PASSWORD']
GAME_IDS = {
    "GroupA": [106917, 106924, 106925, 106919, 106930, 106921, 106922],
    "GroupB": [106915, 106916, 106928, 106929, 106918, 106961, 106920],
    "GroupC": [106912, 106966, 106957, 106967, 106968, 106969, 106963],
    "GroupD": [106953, 106954, 106955, 106956, 106926, 106909, 106908]
}

async def process_game(session, id):
    data = await bgc.load_game_state(session, id)
    return model.make_model(json.loads(data))

async def homepage(request):
    async with ClientSession('http://play.boardgamecore.net') as session:
        await bgc.login(session, BGC_USERNAME, BGC_PASSWORD)
        group_id = request.path_params['group']
        data = await asyncio.gather(*[process_game(session, id) for id in GAME_IDS[group_id]])
        return templates.TemplateResponse(
            'dashboard.html', {'request': request, 'games': data},
            headers={'Cache-Control':'max-age=900, public'}
        )

app = Starlette(routes=[
    Route('/Winter22/{group}', homepage)
])
