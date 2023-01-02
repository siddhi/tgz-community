from dataclasses import dataclass
from itertools import chain

@dataclass
class PlayerRanking:
    name: str
    wins: int
    diffs: tuple[int]


def calculate_wins(name, completed_games):
    return len([game for game in completed_games if game.winner.name == name])

def get_player(name, game):
    for player in game.players:
        if player.name == name:
            return player
    assert None, f"{name} not in {game.players}"

def calculate_diff(name, game):
    player = get_player(name, game)
    winner = get_player(game.winner.name, game)
    return player.vp_delta - winner.vp_delta

def has_player(name, game):
    return name in [player.name for player in game.players]


def calculate_diffs(name, completed_games):
    lost_games = [game for game in completed_games if name != game.winner.name and has_player(name, game)]
    return sorted([calculate_diff(name, game) for game in lost_games], reverse=True)

def make_player_ranking(name, games):
    completed_games = [game for game in games if game.game_info.is_complete]
    wins = calculate_wins(name, completed_games)
    diffs = calculate_diffs(name, completed_games)
    return PlayerRanking(name, wins=wins, diffs=tuple(diffs))

def get_all_players_in_all_games(games):
    return chain(*[game.players for game in games])

def make_ranking(games):
    players = set(player.name for player in get_all_players_in_all_games(games))
    return {player: make_player_ranking(player, games) for player in players}
