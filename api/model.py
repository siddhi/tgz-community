from .parser import BGCDecoder
from typing import Optional
from datetime import datetime
from itertools import groupby
from more_itertools import sliced
from collections import Counter
from dataclasses import dataclass
from enum import Enum


class GamePhase(Enum):
    SETUP = 0
    BID = 1
    ACTIONS = 2
    INCOME = 3
    CHECK_END = 4
    END_GAME = 5

class God(Enum):
    NO_GOD = -1
    XANGO = 0
    QAMATA = 1
    DZIVA = 2
    TSUI_GOAB = 3
    ELEGUA = 4
    GU = 5
    SHADIPINYI = 6
    ESHU = 7
    ENGAI = 8
    ANANSI = 9
    ATETE = 10
    OBATALA = 11


@dataclass(frozen=True)
class Player:
    name: str
    turn_order: int
    vr: int = 20
    vp: int = 0
    god: God = God.NO_GOD
    
    @property
    def vp_delta(self):
        return self.vp - self.vr

@dataclass(frozen=True)
class GameInfo:
    phase: GamePhase = GamePhase.SETUP
    last_move: Optional[datetime] = None

    @property
    def is_complete(self):
        return self.phase == GamePhase.END_GAME

@dataclass(frozen=True)
class DashboardModel:
    id: int
    name: str
    players: list[Player]
    current_player: str
    game_info: GameInfo

    def _rank_players(self, player):
        """order in which conditions have to be checked (bigger number is ahead in rank)
           1. VP - VR
           2. Xango breaks ties
           3. VP
           4. Earlier in turn order
        """
        return (player.vp_delta, 
                1 if player.god == God.XANGO else 0, 
                player.vp,
                -player.turn_order)

    @property
    def winner(self):
        if not self.game_info.is_complete:
            return None

        sorted_players = sorted(self.players, key=self._rank_players, reverse=True)
        return sorted_players[0]

    
def get_names(player_table):
    return [player[0] for player in player_table]

def get_vrs(player_count, vr_table):
    if vr_table is None:
        return [20] * player_count
    player_info = sliced(vr_table, 3)
    sorted_player_info = sorted(player_info, key=lambda info: info[0])
    return [player_info[1] for player_info in sorted_player_info]

def get_god(player):
    god = player[2]
    if god is None:
        return God.NO_GOD
    return God(player[2])

def get_gods(player_table):
    return [get_god(player) for player in player_table]

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
    if craft_table is None:
        return [[0, 0, 0, 0, 0, 0, 0] for player_id in range(player_count)]
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

def get_turn_order(game_state_table):
    turn_order = game_state_table[3]
    return [turn_order.index(player_id) for player_id in range(len(turn_order))]

def get_player_info_from_table(table):
    player_table = table[0]
    monument_table = table[1]
    craft_table = table[2]
    vr_table = table[19]
    game_state_table = table[12]
    names = get_names(player_table)
    gods = get_gods(player_table)
    vrs = get_vrs(len(player_table), vr_table)
    vps = get_vps(len(player_table), monument_table, craft_table) 
    turn_order = get_turn_order(game_state_table)

    data = zip(names, turn_order, vrs, vps, gods)
    return [Player(*fields) for fields in data]

def get_last_move_time(log_table, timestamp_table):
    start_timestamp = log_table[0]
    last_move_delta = timestamp_table[-1]
    return datetime.utcfromtimestamp(start_timestamp + last_move_delta)

def get_game_state(table):
    game_state_table = table[12]
    log_table = table[17]
    timestamp_table = table[18]
    last_move = get_last_move_time(log_table, timestamp_table)
    return GameInfo(
        phase=GamePhase(game_state_table[1]),
        last_move=last_move
    )

def make_model(raw_data):
    try:
        load = raw_data['load']
    except KeyError:
        players = [Player(player, turn_order) for turn_order, player in enumerate(raw_data['players'])]
        game_info = GameInfo()
    else:
        table = BGCDecoder.parse_string(load)[0]
        players = get_player_info_from_table(table)
        game_info = get_game_state(table)
        
    return DashboardModel(
        id=raw_data['gameId'],
        name=raw_data['gameName'],
        players=players,
        current_player=raw_data['currentPlayers'],
        game_info = game_info
    )
