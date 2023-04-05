import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from aiohttp import ClientSession
from . import bgc, model, filters, ranking
import json
import os

templates = Jinja2Templates(directory='templates')
templates.env.filters['humanise'] = filters.humanise
templates.env.filters['underscore_to_space'] = filters.underscore_to_space
templates.env.filters['pad_tuple'] = filters.pad_tuple

BGC_USERNAME = os.environ['BGC_USERNAME']
BGC_PASSWORD = os.environ['BGC_PASSWORD']
GAME_IDS = {
    'Summer23': {
        'GroupA': [109048, 109104, 109468, 109071, 109501, 109051, 109072],
        'GroupB': [109024, 109084, 109081, 109025, 109082, 109026, 109027],
        'GroupC': [109113, 109029, 109030, 109114, 109037, 109115, 109116],
        'GroupD': [109092, 109093, 109094, 109095, 109052, 109044, 109045],
        'GroupE': [109046, 109040, 109047, 109041, 109042, 109043, 109078],
        'GroupF': [109061, 109062, 109057, 109058, 109059, 109064, 109060],
    },
    'Winter22': {
        "GroupA": [106917, 106924, 106925, 106919, 106930, 106921, 106922],
        "GroupB": [106915, 106916, 106928, 106929, 106918, 106961, 106920],
        "GroupC": [106912, 106966, 106957, 106967, 106968, 106969, 106963],
        "GroupD": [106953, 106954, 106955, 106956, 106926, 106909, 106908],
        "GroupE": [107694, 107722, 107709, 107695, 107710, 107696, 107697],
        "GroupF": [107701, 107706, 107702, 107707, 107703, 107704, 107810],
        "Final": [108119]
    }
}

async def process_game(session, id):
    data = await bgc.load_game_state(session, id)
    return model.make_model(json.loads(data))

async def homepage(request):
    async with ClientSession('http://play.boardgamecore.net') as session:
        await bgc.login(session, BGC_USERNAME, BGC_PASSWORD)
        tournament = request.path_params['tournament']
        group_name = request.path_params['group']
        ids = GAME_IDS[tournament][group_name]
        games = await asyncio.gather(*[process_game(session, id) for id in ids])
        player_rankings = ranking.make_ranking(games)
        return templates.TemplateResponse(
            'dashboard.html', {
                'request': request, 
                'group_name': group_name, 
                'games': games,
                'ranking': player_rankings
            },
            headers={'Cache-Control':'max-age=900, public'}
        )

app = Starlette(routes=[
    Route('/{tournament}/{group}', homepage)
])
