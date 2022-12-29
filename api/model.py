from more_itertools import sliced
from dataclasses import dataclass
from .parser import BGCDecoder

@dataclass
class Player:
    name: str
    vr: int

@dataclass
class DashboardModel:
    id: int
    name: str
    players: list[Player]
    current_player: str

def get_names(player_table):
    return[player[0] for player in player_table]

def get_vrs(vr_table):
    player_info = sliced(vr_table, 3)
    sorted_player_info = sorted(player_info, key=lambda info: info[0])
    return [player_info[1] for player_info in sorted_player_info]

def get_player_info_from_table(table):
    player_table = table[0]
    vr_table = table[19]
    names = get_names(player_table)
    vrs = get_vrs(vr_table)
    data = zip(names, vrs)
    return [Player(*fields) for fields in data]

def make_model(raw_data):
    try:
        load = raw_data['load']
    except KeyError:
        players = [Player(player, 20) for player in raw_data['players']]
    else:
        table = BGCDecoder.parse_string(load)[0]
        players = get_player_info_from_table(table)
    return DashboardModel(
        id=raw_data['gameId'],
        name=raw_data['gameName'],
        players=players,
        current_player=raw_data['currentPlayers']
    )
