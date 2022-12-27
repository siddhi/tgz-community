from asyncio import wait
from dataclasses import dataclass

@dataclass
class BGCModel:
    id: int
    name: str
    players: list[str]
    current_player: str

def make_model(raw_data):
    return BGCModel(
        id=raw_data['gameId'],
        name=raw_data['gameName'],
        players=raw_data['players'],
        current_player=raw_data['currentPlayers']
    )
