
async def login(session, username, password):
    async with session.post('http://play.boardgamecore.net/login.jsp', data={'login':username, 'password':password}) as resp:
        data = await resp.text()
        assert 'ok' in data

