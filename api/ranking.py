from dataclasses import dataclass
from itertools import chain

@dataclass
class PlayerRanking:
    name: str
    wins: int

def make_player_ranking(name, games):
    wins = len([game for game in games if game.game_info.is_complete and game.winner.name == name])
    return PlayerRanking(name, wins=wins)

def get_players(games):
    return chain(*[game.players for game in games])

def make_ranking(games):
    players = set(player.name for player in get_players(games))
    return [make_player_ranking(player, games) for player in players]
