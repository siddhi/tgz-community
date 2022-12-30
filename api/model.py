from .parser import BGCDecoder
from itertools import groupby
from more_itertools import sliced
from collections import Counter
from dataclasses import dataclass
from enum import Enum


class GameState(Enum):
    SETUP = 0
    BID = 1
    ACTIONS = 2
    INCOME = 3
    CHECK_END = 4
    END_GAME = 5

@dataclass
class Player:
    name: str
    vr: int
    vp: int
    
    @property
    def vp_delta(self):
        return self.vp - self.vr

@dataclass
class DashboardModel:
    id: int
    name: str
    players: list[Player]
    current_player: str
    game_state: GameState
    
    @property
    def is_complete(self):
        return self.game_state == GameState.END_GAME

def get_names(player_table):
    return[player[0] for player in player_table]

def get_vrs(vr_table):
    player_info = sliced(vr_table, 3)
    sorted_player_info = sorted(player_info, key=lambda info: info[0])
    return [player_info[1] for player_info in sorted_player_info]

MONUMENT_POINTS = [1, 3, 7, 13, 21]

def calculate_monument_vp(momument_counts):
    return sum(points * count for points, count in zip(MONUMENT_POINTS, momument_counts))

CRAFT_POINTS = [1, 1, 1, 3, 2, 2, 2]

def calculate_craft_vp(craft_counts):
    return sum(points * count for points, count in zip(CRAFT_POINTS, craft_counts))

def get_monuments_count_for_player(group):
    monuments = [item[2] for item in group]
    counts = Counter(monuments)
    return [counts[monument_level] for monument_level in range(1, 6)]

def get_craft_count_for_player(group):
    crafts = [item[2] for item in group]
    counts = Counter(crafts)
    return [counts[craft_type] for craft_type in range(7)]

def get_player_monument_counts(monument_table):
    monument_details = sliced(monument_table, 3)
    sort_by_player = lambda item: item[0] # first element is player number
    data = sorted(monument_details, key=sort_by_player)
    return [get_monuments_count_for_player(group) for key, group in groupby(data, key=sort_by_player)]

def get_player_craft_counts(player_count, craft_table):
    craft_details = sliced(craft_table, 4)
    sort_by_player = lambda item: item[0] # first element is player number
    data = groupby(sorted(craft_details, key=sort_by_player), key=sort_by_player)
    craft_by_player = {key:get_craft_count_for_player(group) for key, group in data}
    return [craft_by_player.get(player_id, [0]*7) for player_id in range(player_count)]

def calculate_total_vp(monument_counts, craft_counts):
    return calculate_monument_vp(monument_counts) + calculate_craft_vp(craft_counts)

def get_vps(player_count, monument_table, craft_table):
    monument_counts = get_player_monument_counts(monument_table)
    craft_counts = get_player_craft_counts(player_count, craft_table)
    vp_data = zip(monument_counts, craft_counts)
    return [calculate_total_vp(*vp_fields) for vp_fields in vp_data]

def get_player_info_from_table(table):
    player_table = table[0]
    monument_table = table[1]
    craft_table = table[2]
    vr_table = table[19]
    names = get_names(player_table)
    vrs = get_vrs(vr_table)
    vps = get_vps(len(player_table), monument_table, craft_table) 

    data = zip(names, vrs, vps)
    return [Player(*fields) for fields in data]

def get_game_state(table):
    game_state_table = table[12]
    return GameState(game_state_table[1])

def make_model(raw_data):
    try:
        load = raw_data['load']
    except KeyError:
        players = [Player(player, vr=20, vp=0) for player in raw_data['players']]
        game_state = GameState.SETUP
    else:
        table = BGCDecoder.parse_string(load)[0]
        players = get_player_info_from_table(table)
        game_state = get_game_state(table)
        
    return DashboardModel(
        id=raw_data['gameId'],
        name=raw_data['gameName'],
        players=players,
        current_player=raw_data['currentPlayers'],
        game_state = game_state
    )
