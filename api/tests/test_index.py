from starlette.testclient import TestClient
import os
os.environ['BGC_USERNAME'] = 'testuser'
os.environ['BGC_PASSWORD'] = 'testpass'
import json

from api.index import app
import pytest
from aioresponses import aioresponses

@pytest.fixture
def game_response():
    data = {'gameId': 123, 'gameName': 'Sample game', 'load': '[[[$player1@2@6??@3?][$player2@0@3-130-1420d10@l?][$player3@3?-12000-1030a30320520@n?][$player4@1@7?-1220c20@c?]]-2001T02013c04023f03032J02003M03013Q03003A03032H02012702002n02032l02031O01023k02031e01-2032*0100013O02010230000103280600012E0600022Y050002110000023R0500020q0100021L0100021%020002490200-22Q042y044k044l043704-21U012M00?-11003311[&1@4@4@4]@a-1245ab-114-11002210[@9@1@3-12130]$54b201931372012161[?-12112]??[@1zCIPz[@%@0[$54b201931372012161]][@0@1-21T][@1@1-23c][@2@1-23f][@3@1-22J][@%@b-11][@3@2-11][@2@2+11][@1@2+11][@0@2+11][@3@a-12][@3@d-22*010002][@3@e[-122]][@0@a-10][@0@1-23M][@1@a-12][@1@d-23O020104][@1@e[-142]][@2@5-12][@2@7-122][@2@g-1210010312110][@%@b-12][@1@2-11][@3@2+11][@2@2+11][@0@2+11][@1@3?][@1@4-13][@1@a-10][@1@1-23Q][@0@a-11][@0@c[@1T@2-11-22*2u@0]][@0@c[@3M@2-12-23O3i@0]][@2@7-122][@2@a-12][@2@d-230000100][@2@e[-102]][@3@a-11][@3@c[@2J@2-11-22*3N@0]][@3@g-1220012314124][@%@b-13][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-11][@1@c[@3Q@2-12-23O3i@0]][@1@c[@3c@2-12-23O3T@0]][@0@a-10][@0@1-23A][@3@a-12][@3@d-22806000c][@3@e[-122c2]][@2@5-10][@2@7-103][@2@8-21U01][@2@a-11][@2@c[@3f@2-10-2303W@0]][@2@g-1220024325120][@%@b-14][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-12][@1@d-22E06000d][@1@e[-142d1]][@1@5-13][@1@7-132][@1@9-22Q04][@0@a-11][@0@c[@3M@3-110-2303W@0]][@3@a-10][@3@1-22H][@2@7-122][@2@a-12][@2@d-22Y05000a][@2@e[-103a2]][@2@g-1230022326122][@%@b-15][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-10][@1@1-227][@1@7-132][@1@9-22y04][@0@a-10][@0@1-22n][@3@a-10][@3@1-22l][@3@4-17][@2@7-122][@2@a-12][@2@d-2110000][@2@d-23R0500][@2@e[-1a3]][@2@g-1230022326120][@%@b-16][@1@2-11][@2@2+11][@3@2-12][@0@2+11][@1@2+11][@3@a-11][@3@c[@2l@2-16-228453O4n@0]][@3@c[@2H@2-16-2283T3O3i@0]][@1@7-132][@1@9-24k04][@1@a-11][@1@c[@27@2-16-22E2G3O4k@0]][@0@4-16][@0@a-11][@0@c[@3A@2-10-2303W@0]][@2@7-122][@2@a-12][@2@d-1q103][@2@d-21L0100][@2@d-21%020005][@2@d-2490200][@2@e[-13252]][@2@g-123002932d124][@%@b-17][@2@2+11][@1@2+11][@3@2+11][@0@a-11][@0@c[@3A@3-160-2302p@0]][@3@a-10][@3@1-21O][@1@7-132][@1@9-24l04][@1@a-11][@1@c[@3c@3-166-22E2y3O4n@0]][@2@a-10][@2@1-23k][@2@g-123003b323120][@%@b-18][@2@2-11][@1@2-12][@3@2+11][@0@2-13][@2@2+11][@1@2+11][@0@3?][@0@a-11][@0@c[@2n@2-16-22E2G3O45@0]][@1@a-11][@1@c[@3c@4-1666-22E363O4l@0]][@1@c[@3Q@3-160-2302p@0]][@1@7-132][@1@9-23704][@2@7-103][@2@8-22M00][@2@a-11][@2@c[@3k@2-10-2110s@0]][@2@c[@3f@3-106-22E37494M@1]][@3@a-10][@3@1-21e][@3@g-123004i33e120][@%@b-19][@2@2-11][@1@2-12]]-40000000s00iO05V%0fW20fW40fWb0iQc0lgR0lrW0l*l0l*p0l*r0myI0mz00mDr0mDB0mDG0mIk0mIk0mIH0mIH0mPl0B3u0Ctj0GyD0GyE0GFK0GFO0GFQ0HjF0HjJ0HjX0U9c0U9g0U9o0U9w0WIj0WIT0WJY0WJY0*Xv107n16S%18691885188a188e18m818me1BF51BFc1BGo1CDS1CDS1CE51CEp1CEt1CED1CED1E*P1Geh1XQk1YJI1*Jl1*Jv1*JG1*KI1*KI1*KR20vL20w72edL2edQ2f6r2f6u2f7g2f7t2f7*2f7*2k6h2muM2szB2E0n2E502E5c2E5k2E5n2GQd2GQU2J7N2J9U2Jaj2L4I2L4M2L502L5v2L5y2L5P2L5P2LbA2Ls92No32YRK2ZW%30Wc30WV30Ya311L311U3129312n32rM32rW32sH33rY33r%33s933sd33sz33sK33sO33te33te33tB3cgr3jrP3jX83jX%3njv3njD3nzZ3nA03nA23nAv3nFt3nG93nGt3nGt3nGF3y623Gdc3GTD3HgF3HL23HL33K1M3K2h3Qsc3QsF3QtV3Qt*3QuS3T1x3T1N3T1S3T2t3T3J3Uy63Uyi3Uys3Uys3VB43YWJ-13t02A01x00o0]', 'players': ['player1', 'player2', 'player3', 'player4'], 'chat': [], 'now': 1672129004299, 'currentPlayers': 'player4', 'name': 'player4'}
    return json.dumps(data)

@pytest.fixture
def bgc_api(game_response):
    with aioresponses() as api:
        api.post('/login.jsp', status=200, body='ok')
        api.post('/Json', status=200, body=game_response, repeat=True)
        yield api

@pytest.fixture
def client():
    return TestClient(app)


def test_homepage_returns_success(client, bgc_api):
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_passes_required_context(client, bgc_api):
    response = client.get('/')
    assert 'games' in response.context
