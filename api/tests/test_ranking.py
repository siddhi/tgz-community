from api.model import DashboardModel, GameInfo, Player
from api.ranking import make_ranking

import pytest

from api.model import GamePhase

@pytest.fixture
def in_progress_game():
    p1 = Player(name='p1', vp=12, vr=22, turn_order=0)
    p2 = Player(name='p2', vp=21, vr=23, turn_order=1)
    p3 = Player(name='p3', vp=16, vr=29, turn_order=2)
    p4 = Player(name='p4', vp=26, vr=35, turn_order=3)
    return DashboardModel(
        id=1,
        name='sample game',
        players=[p1, p2, p3, p4],
        game_info=GameInfo(phase=GamePhase.ACTIONS),
        current_player='p1'
    )

@pytest.fixture
def game1():
    p1 = Player(name='p1', vp=25, vr=22, turn_order=0) # winner
    p2 = Player(name='p2', vp=23, vr=23, turn_order=1) # diff -3
    p3 = Player(name='p3', vp=16, vr=29, turn_order=2) # diff -16
    p4 = Player(name='p4', vp=26, vr=35, turn_order=3) # diff -12
    return DashboardModel(
        id=1,
        name='sample game',
        players=[p1, p2, p3, p4],
        game_info=GameInfo(phase=GamePhase.END_GAME),
        current_player='p1'
    )

@pytest.fixture
def game2():
    p1 = Player(name='p1', vp=30, vr=30, turn_order=0) # winner
    p2 = Player(name='p2', vp=21, vr=26, turn_order=1) # diff -5
    p5 = Player(name='p5', vp=31, vr=33, turn_order=2) # diff -2
    p6 = Player(name='p6', vp=13, vr=20, turn_order=3) # diff -7
    return DashboardModel(
        id=1,
        name='sample game',
        players=[p1, p2, p5, p6],
        game_info=GameInfo(phase=GamePhase.END_GAME),
        current_player='p1'
    )


@pytest.fixture
def game3():
    p3 = Player(name='p3', vp=10, vr=20, turn_order=0) # diff -12
    p4 = Player(name='p4', vp=22, vr=28, turn_order=1) # diff -8
    p5 = Player(name='p5', vp=32, vr=30, turn_order=2) # winner
    p6 = Player(name='p6', vp=16, vr=25, turn_order=3) # diff -11
    return DashboardModel(
        id=1,
        name='sample game',
        players=[p3, p4, p5, p6],
        game_info=GameInfo(phase=GamePhase.END_GAME),
        current_player='p1'
    )


def test_ranking_should_include_all_players(game1):
    ranking = make_ranking([game1])
    assert len(ranking) == 4

def test_ranking_should_include_all_players_across_games(game1, game2):
    ranking = make_ranking([game1, game2])
    assert len(ranking) == 6

def test_should_calculate_each_players_wins(game1, game2, game3):
    ranking = make_ranking([game1, game2, game3])
    wins = [(player.name, player.wins) for player in ranking.values()]
    assert set(wins) == {('p1', 2), ('p2', 0), ('p3', 0), ('p4', 0), ('p5', 1), ('p6', 0)}

def test_should_ignore_games_in_progress(game1, in_progress_game):
    ranking = make_ranking([game1, in_progress_game])
    wins = [(player.name, player.wins) for player in ranking.values()]
    assert set(wins) == {('p1', 1), ('p2', 0), ('p3', 0), ('p4', 0)}

def test_should_calculate_delta_difference_against_winner(game1, game2, game3):
    """if the winner got vp-vr of +2 and this player got vp-vr of -3 then
    the delta diff for the player in this game is -5 behind the winner"""
    ranking = make_ranking([game1, game2, game3])
    assert set(ranking['p1'].diffs) == set()
    assert set(ranking['p2'].diffs) == {-3, -5}
    assert set(ranking['p3'].diffs) == {-12, -16}
    assert set(ranking['p4'].diffs) == {-8, -12}
    assert set(ranking['p5'].diffs) == {-2}
    assert set(ranking['p6'].diffs) == {-7, -11}

def test_delta_differences_should_be_sorted(game1, game2, game3):
    ranking = make_ranking([game1, game2, game3])
    assert ranking['p3'].diffs == (-12, -16)
