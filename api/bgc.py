async def login(session, username, password):
    async with session.post('/login.jsp', data={'login':username, 'password':password}) as resp:
        data = await resp.text()
        assert 'ok' in data

async def load_game_state(session, game_id):
    async with session.post('/Json', data={'id': game_id, 'action':'initLoad'}) as resp:
        return await resp.text()
