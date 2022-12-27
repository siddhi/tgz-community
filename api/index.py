from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

async def homepage(request):
    games = []
    return templates.TemplateResponse('dashboard.html', {'request': request, 'games': games})

app = Starlette(routes=[
    Route('/', homepage)
])
