import pytest

from api.model import make_model

@pytest.fixture
def basic_response():
    return {
        'gameId': 1234, 'gameName': 'Game 123', 
        'players': ['player 1', 'player 2', 'player 3', 'player 4'],
        'currentPlayers': 'player 4'
    }

def test_model_extracts_game_id(basic_response):
    model = make_model(basic_response)
    assert model.id == 1234

def test_model_extracts_game_name(basic_response):
    model = make_model(basic_response)
    assert model.name == 'Game 123'

def test_model_extracts_player_names(basic_response):
    model = make_model(basic_response)
    assert model.players == ['player 1', 'player 2', 'player 3', 'player 4']

def test_model_extractr_current_player(basic_response):
    model = make_model(basic_response)
    assert model.current_player == 'player 4'


