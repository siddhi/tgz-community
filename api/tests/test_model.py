import pytest
from datetime import datetime

from api.model import (God, GamePhase, GameInfo, Player, DashboardModel,
                       make_model, calculate_monument_vp, calculate_craft_vp)

@pytest.fixture
def basic_response():
    return {
        'gameId': 1234, 'gameName': 'Game 123', 
        'players': ['player1', 'player2', 'player3', 'player4'],
        'currentPlayers': 'player 4'
    }


def test_model_extracts_game_id(basic_response):
    model = make_model(basic_response)
    assert model.id == 1234

def test_model_extracts_game_name(basic_response):
    model = make_model(basic_response)
    assert model.name == 'Game 123'

def test_model_extracts_current_player(basic_response):
    model = make_model(basic_response)
    assert model.current_player == 'player 4'

def test_model_extracts_player_names_without_game_state(basic_response):
    model = make_model(basic_response)
    names = [player.name for player in model.players]
    assert names == ['player1', 'player2', 'player3', 'player4']
    
def test_model_has_game_state_setup_at_first(basic_response):
    model = make_model(basic_response)
    assert model.game_info.phase == GamePhase.SETUP

@pytest.fixture
def response_with_game_state():
    return {
        'gameId': 1234, 'gameName': 'Game 123', 
        'players': ['player 1', 'player 2', 'player 3', 'player 4'],
        'currentPlayers': 'player 4',
        'load': '[[[$player1@2@6??@3?][$player2@0@3-130-1420d10@l?][$player3@3?-12000-1030a30320520@n?][$player4@1@7?-1220c20@c?]]-2001T02013c04023f03032J02003M03013Q03003A03032H02012702002n02032l02031O01023k02031e01-2032*0100013O02010230000103280600012E0600022Y050002110000023R0500020q0100021L0100021%020002490200-22Q042y044k044l043704-21U012M00?-11003311[&1@4@4@4]@a-1245ab-114-11002210[@9@5@3-12130]$54b201931372012161[?-12112]??[@1zCIPz[@%@0[$54b201931372012161]][@0@1-21T][@1@1-23c][@2@1-23f][@3@1-22J][@%@b-11][@3@2-11][@2@2+11][@1@2+11][@0@2+11][@3@a-12][@3@d-22*010002][@3@e[-122]][@0@a-10][@0@1-23M][@1@a-12][@1@d-23O020104][@1@e[-142]][@2@5-12][@2@7-122][@2@g-1210010312110][@%@b-12][@1@2-11][@3@2+11][@2@2+11][@0@2+11][@1@3?][@1@4-13][@1@a-10][@1@1-23Q][@0@a-11][@0@c[@1T@2-11-22*2u@0]][@0@c[@3M@2-12-23O3i@0]][@2@7-122][@2@a-12][@2@d-230000100][@2@e[-102]][@3@a-11][@3@c[@2J@2-11-22*3N@0]][@3@g-1220012314124][@%@b-13][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-11][@1@c[@3Q@2-12-23O3i@0]][@1@c[@3c@2-12-23O3T@0]][@0@a-10][@0@1-23A][@3@a-12][@3@d-22806000c][@3@e[-122c2]][@2@5-10][@2@7-103][@2@8-21U01][@2@a-11][@2@c[@3f@2-10-2303W@0]][@2@g-1220024325120][@%@b-14][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-12][@1@d-22E06000d][@1@e[-142d1]][@1@5-13][@1@7-132][@1@9-22Q04][@0@a-11][@0@c[@3M@3-110-2303W@0]][@3@a-10][@3@1-22H][@2@7-122][@2@a-12][@2@d-22Y05000a][@2@e[-103a2]][@2@g-1230022326122][@%@b-15][@1@2-11][@2@2+11][@3@2+11][@0@2+11][@1@a-10][@1@1-227][@1@7-132][@1@9-22y04][@0@a-10][@0@1-22n][@3@a-10][@3@1-22l][@3@4-17][@2@7-122][@2@a-12][@2@d-2110000][@2@d-23R0500][@2@e[-1a3]][@2@g-1230022326120][@%@b-16][@1@2-11][@2@2+11][@3@2-12][@0@2+11][@1@2+11][@3@a-11][@3@c[@2l@2-16-228453O4n@0]][@3@c[@2H@2-16-2283T3O3i@0]][@1@7-132][@1@9-24k04][@1@a-11][@1@c[@27@2-16-22E2G3O4k@0]][@0@4-16][@0@a-11][@0@c[@3A@2-10-2303W@0]][@2@7-122][@2@a-12][@2@d-1q103][@2@d-21L0100][@2@d-21%020005][@2@d-2490200][@2@e[-13252]][@2@g-123002932d124][@%@b-17][@2@2+11][@1@2+11][@3@2+11][@0@a-11][@0@c[@3A@3-160-2302p@0]][@3@a-10][@3@1-21O][@1@7-132][@1@9-24l04][@1@a-11][@1@c[@3c@3-166-22E2y3O4n@0]][@2@a-10][@2@1-23k][@2@g-123003b323120][@%@b-18][@2@2-11][@1@2-12][@3@2+11][@0@2-13][@2@2+11][@1@2+11][@0@3?][@0@a-11][@0@c[@2n@2-16-22E2G3O45@0]][@1@a-11][@1@c[@3c@4-1666-22E363O4l@0]][@1@c[@3Q@3-160-2302p@0]][@1@7-132][@1@9-23704][@2@7-103][@2@8-22M00][@2@a-11][@2@c[@3k@2-10-2110s@0]][@2@c[@3f@3-106-22E37494M@1]][@3@a-10][@3@1-21e][@3@g-123004i33e120][@%@b-19][@2@2-11][@1@2-12]]-40000000s00iO05V%0fW20fW40fWb0iQc0lgR0lrW0l*l0l*p0l*r0myI0mz00mDr0mDB0mDG0mIk0mIk0mIH0mIH0mPl0B3u0Ctj0GyD0GyE0GFK0GFO0GFQ0HjF0HjJ0HjX0U9c0U9g0U9o0U9w0WIj0WIT0WJY0WJY0*Xv107n16S%18691885188a188e18m818me1BF51BFc1BGo1CDS1CDS1CE51CEp1CEt1CED1CED1E*P1Geh1XQk1YJI1*Jl1*Jv1*JG1*KI1*KI1*KR20vL20w72edL2edQ2f6r2f6u2f7g2f7t2f7*2f7*2k6h2muM2szB2E0n2E502E5c2E5k2E5n2GQd2GQU2J7N2J9U2Jaj2L4I2L4M2L502L5v2L5y2L5P2L5P2LbA2Ls92No32YRK2ZW%30Wc30WV30Ya311L311U3129312n32rM32rW32sH33rY33r%33s933sd33sz33sK33sO33te33te33tB3cgr3jrP3jX83jX%3njv3njD3nzZ3nA03nA23nAv3nFt3nG93nGt3nGt3nGF3y623Gdc3GTD3HgF3HL23HL33K1M3K2h3Qsc3QsF3QtV3Qt*3QuS3T1x3T1N3T1S3T2t3T3J3Uy63Uyi3Uys3Uys3VB43YWJ-13t02A01x00o0]'
    }

def test_model_extracts_player_names(response_with_game_state):
    model = make_model(response_with_game_state)
    names = [player.name for player in model.players]
    assert names == ['player1', 'player2', 'player3', 'player4']
     
def test_model_extracts_player_vr(response_with_game_state):
    model = make_model(response_with_game_state)
    vrs = [player.vr for player in model.players]
    assert vrs == [24, 33, 36, 29]

def test_model_extracts_player_god(response_with_game_state):
    model = make_model(response_with_game_state)
    gods = [player.god for player in model.players]
    assert gods == [God.SHADIPINYI, God.TSUI_GOAB, God.NONE, God.ESHU]


def test_model_calculates_player_vp(response_with_game_state):
    # Player 0: monument height 2 x 2, height 3 x 2
    # Player 1: monument height 4 x 1, height 3 x 1, height 2 x 1, Wood Carver, Sculptor
    # Player 2: monument height 2 x 1, height 3 x 1, Potter x 2, Throne Maker x 2, Ivory Carver x 2, Wood Carver x 2 
    # Player 3: monument height 1 x 2, height 2 x 3, Ivory Carver, Sculptor
    model = make_model(response_with_game_state)
    vps = [player.vp for player in model.players]
    assert vps == [20, 26, 20, 14]
    

def test_model_extracts_game_state(response_with_game_state):
    model = make_model(response_with_game_state)
    assert model.game_info.phase == GamePhase.END_GAME

def test_model_extracts_last_move_time(response_with_game_state):
    model = make_model(response_with_game_state)
    # unix timestamp in sec, UTC timezone: 1671089379 + 1035949
    assert model.game_info.last_move == datetime(2022, 12, 27, 7, 15, 28)

def test_model_extracts_player_order(response_with_game_state):
    model = make_model(response_with_game_state)
    player_turn_order = [player.turn_order for player in model.players]
    # turn order is player 3, player 2, player 4, player 1
    assert player_turn_order == [3, 1, 0, 2]

def test_calculate_monument_vp_no_monument():
    assert calculate_monument_vp([0, 0, 0, 0, 0]) == 0

def test_calculate_monument_vp_single_monument():
    """a single level one monument"""
    assert calculate_monument_vp([1, 0, 0, 0, 0]) == 1

def test_calculate_monument_vp_multiples_of_single_monument():
    """two level one monuments"""
    assert calculate_monument_vp([2, 0, 0, 0, 0]) == 2

def test_calculate_monument_vp_multiple_monuments():
    """one monument of each level"""
    assert calculate_monument_vp([1, 1, 1, 1, 1]) == 45

def test_calculate_craft_vp_no_craft():
    assert calculate_craft_vp([0, 0, 0, 0, 0, 0, 0]) == 0

def test_calculate_craft_vp_single_craft():
    """a single potter"""
    assert calculate_craft_vp([1, 0, 0, 0, 0, 0, 0]) == 1

def test_calculate_craft_vp_multiple_craft():
    """two throne makers"""
    assert calculate_craft_vp([0, 0, 0, 0, 0, 2, 0]) == 4

def test_calculate_craft_vp_multiple_types():
    """one each"""
    assert calculate_craft_vp([1, 1, 1, 1, 1, 1, 1]) == 12

def test_winner_of_game_in_progress():
    model = DashboardModel(
        id=123,
        name='Game',
        players=[],
        current_player='',
        game_info=GameInfo(phase=GamePhase.ACTIONS)
    )
    assert model.winner == None

def test_winner_is_the_player_above_the_vr():
    p1 = Player(name='p1', turn_order=0, vr=20, vp=16)
    p2 = Player(name='p2', turn_order=1, vr=20, vp=22)
    model = DashboardModel(
        id=123,
        name='Game',
        players=[p1, p2],
        current_player='',
        game_info=GameInfo(phase=GamePhase.END_GAME)
    )
    assert model.winner.name == 'p2'

def test_winner_is_the_player_with_the_highest_delta_above_the_vr():
    p1 = Player(name='p1', turn_order=0, vr=30, vp=37)
    p2 = Player(name='p2', turn_order=1, vr=25, vp=30)
    model = DashboardModel(
        id=123,
        name='Game',
        players=[p1, p2],
        current_player='',
        game_info=GameInfo(phase=GamePhase.END_GAME)
    )
    assert model.winner.name == 'p1'

def test_winner_xango_breaks_tie():
    p1 = Player(name='p1', turn_order=0, vr=35, vp=40, god=God.ANANSI)
    p2 = Player(name='p2', turn_order=1, vr=20, vp=25, god=God.XANGO)
    p3 = Player(name='p3', turn_order=2, vr=30, vp=35)
    model = DashboardModel(
        id=123,
        name='Game',
        players=[p1, p2, p3],
        current_player='',
        game_info=GameInfo(phase=GamePhase.END_GAME)
    )
    assert model.winner.name == 'p2'


def test_winner_on_delta_tie_broken_by_player_with_highest_vr():
    p1 = Player(name='p1', turn_order=0, vr=20, vp=25)
    p2 = Player(name='p2', turn_order=1, vr=35, vp=40)
    p3 = Player(name='p3', turn_order=2, vr=30, vp=35)
    model = DashboardModel(
        id=123,
        name='Game',
        players=[p1, p2, p3],
        current_player='',
        game_info=GameInfo(phase=GamePhase.END_GAME)
    )
    assert model.winner.name == 'p2'

def test_winner_all_ties_broken_by_player_order():
    p1 = Player(name='p1', turn_order=0, vr=20, vp=25)
    p2 = Player(name='p2', turn_order=2, vr=35, vp=40)
    p3 = Player(name='p3', turn_order=1, vr=35, vp=40)
    model = DashboardModel(
        id=123,
        name='Game',
        players=[p1, p2, p3],
        current_player='',
        game_info=GameInfo(phase=GamePhase.END_GAME)
    )
    assert model.winner.name == 'p3'

