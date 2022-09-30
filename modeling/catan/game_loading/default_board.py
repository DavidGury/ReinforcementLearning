from dataclasses import dataclass, field, InitVar
from hex_board import HexBoard, TileType, TileInfo
from catan_objects import Terrain, Space, Environment, Building, TradeShip, CatanBoardObject
from gamedata import board
from typing import Optional, Annotated
import itertools
from collections import namedtuple
from enum import Enum
import random
import tools


TILE_TYPE_CONV = {
    TileType.Hex: Space.Hex,
    TileType.Intersection: Space.Intersection,
    TileType.PathVertical: Space.Path,
    TileType.PathSlopedL: Space.Path,
    TileType.PathSlopedR: Space.Path
}

S, L = Environment.Sea, Environment.Land
HEX_ENVS = [
    [S, S, S, S, S, S, S],
    [S, S, L, L, L, S, S],
    [S, S, L, L, L, L, S],
    [S, L, L, L, L, L, S],
    [S, S, L, L, L, L, S],
    [S, S, L, L, L, S, S],
    [S, S, S, S, S, S, S]
]


OBJECT_DEFAULTS = {
    Space.Hex: Terrain.NoTerrain,
    Space.Intersection: Building.NoBuilding,
    Space.Path: Building.NoBuilding
}

TRADE_TILE_GROUP_SIZE = 3
NUM_TRADE_GROUPS = 6
NUM_TRADE_TILES = TRADE_TILE_GROUP_SIZE * NUM_TRADE_GROUPS
TradePieceSize = lambda tile_type: Annotated[tuple[tile_type], NUM_TRADE_GROUPS]
TradePieceCount = lambda piece_type: Annotated[tuple[piece_type], NUM_TRADE_GROUPS]


TRADE_SHIP_TILES = [
    (TradeShip.AllShip, TradeShip.NoTradeShip, TradeShip.GrainShip),
    (TradeShip.NoTradeShip, TradeShip.OreShip, TradeShip.NoTradeShip),
    (TradeShip.AllShip, TradeShip.NoTradeShip, TradeShip.WoolShip),
    (TradeShip.NoTradeShip, TradeShip.AllShip, TradeShip.NoTradeShip),
    (TradeShip.AllShip, TradeShip.NoTradeShip, TradeShip.BrickShip),
    (TradeShip.NoTradeShip, TradeShip.LumberShip, TradeShip.NoTradeShip)
]

TRADE_SHIP_PLACEMENTS = [
    (2, 3, 4),
    (5, 12, 20),
    (27, 34, 40),
    (47, 46, 45),
    (44, 36, 29),
    (21, 15, 8)
]


ISEC_CONNS_READING_ORDER = i_N, i_NW, i_NE, i_SW, i_SE, i_S = range(6)


TOP, TOP_L, TOP_R, BOT_L, BOT_R, BOT = range(6)
SEA_HEX_CONNECTIONS: dict[tuple[int, ...], list[int]] = {
    (2, 3, 8): [BOT_R, BOT],
    (4, 5, 12): [BOT_L, BOT],
    (20, 27, 34): [TOP_L, BOT_L],
    (40, 46, 47): [TOP, TOP_L],
    (36, 44, 45): [TOP, TOP_R],
    (15, 21, 29): [TOP_R, BOT_R]
}


@dataclass
class ConvertedTile:
    index: int
    space: Space
    connections: list[int]
    loc: tuple[int, int]
    chit_value: int = 0
    env: Environment = Environment.Land
    object: CatanBoardObject = field(init=False)

    def __post_init__(self):
        self.object = OBJECT_DEFAULTS[self.space]


class DockOrientation(Enum):
    NW = (i_N, i_NW), '\\|.\n...'
    NE = (i_N, i_NE), '.|/\n...'
    W = (i_NW, i_SW), '\\..\n/..'
    E = (i_NE, i_SE), '../\n..\\'
    SW = (i_S, i_SW), '...\n/|.'
    SE = (i_S, i_SE), '...\n.|\\'

    def __init__(self, connections: tuple[int, int], rep: str = '...\n...'):
        """
        :param connections: Two integers between 0 and 5, representing Hex tile intersection connections
            (indexed in reading order).
        """
        self.validate_connections(connections)
        self.connections = connections
        self._rep = rep

    @staticmethod
    def validate_connections(connections: tuple[int, int]):
        if all(0 <= c < 6 for c in connections):
            return
        raise ValueError(f'Dock connections must be values between 0 and 5.')


@dataclass
class TradeTile:
    tile_index: int
    dock_orientation: DockOrientation


@dataclass
class TradeTileLoadout:
    TradeTileSlots: TradePieceCount(TradePieceSize(TradeTile))
    TradeShips: TradePieceCount(TradePieceSize(TradeShip))

    # TODO - trade tile loadout, also make one for terrains/chits

    def get_trade_tiles(self) -> Annotated[tuple[ConvertedTile], NUM_TRADE_TILES]:
        ...



#  Use Hex board to generate both BoardData and GameDisplay
def make_default_board():
    def get_connected_envs(tile: ConvertedTile, space_type: Space) -> list[Environment]:
        return [tile_data[tc].env for tc in tile.connections if tile_data[tc].space == space_type]

    def update_hex_environments() -> None:
        for i, env in enumerate(itertools.chain.from_iterable(HEX_ENVS)):
            tile_data[i].env = env

    def update_intersection_environments() -> None:
        for t in tile_data:
            if t.space != Space.Intersection:
                continue
            conn_envs = get_connected_envs(t, Space.Hex)
            if Environment.Sea not in conn_envs:
                t.env = Environment.Land
            elif Environment.Land not in conn_envs:
                t.env = Environment.Sea
            else:
                t.env = Environment.Coast

    def update_path_environments() -> None:
        for t in tile_data:
            if t.space != Space.Path:
                continue
            conn_envs = get_connected_envs(t, Space.Intersection)
            if Environment.Land in conn_envs:
                t.env = Environment.Land
            elif Environment.Sea in conn_envs:
                t.env = Environment.Sea
            else:
                t.env = Environment.Coast

    def update_sea_connections() -> None:
        for trade_tiles, conns in SEA_HEX_CONNECTIONS.items():
            for i in trade_tiles:
                c = tile_data[i].connections
                tile_data[i].connections = [c[k] for k in conns]
    #
    hb = HexBoard(
        resolution=(1920, 1080),
        n_hexes_yaxis=len(HEX_ENVS),
        n_hexes_xaxis=len(HEX_ENVS[0]),
        margin=5
    )

    tile_data = [
        ConvertedTile(
            index=tile.index,
            space=TILE_TYPE_CONV[tile.tile_type],
            connections=sorted(tile.connections),
            loc=tile.loc
        ) for tile in hb.tiles]

    update_hex_environments()
    update_intersection_environments()
    update_path_environments()
    update_sea_connections()

    return tile_data


ROBBER_STARTS_ON = Terrain.Desert
TERRAIN_COUNTS = {
    Terrain.Hill: 3,
    Terrain.Forest: 4,
    Terrain.Pasture: 4,
    Terrain.Field: 4,
    Terrain.Mountain: 3,
    Terrain.Desert: 1
}
CHITS = {c: 2 if c not in (2, 12) else 1 for c in range(2, 13)}


def randomize_chits_terrains():
    terrain_pile = list(itertools.chain.from_iterable([terr]*qty for terr, qty in TERRAIN_COUNTS.items()))
    chit_pile = list(itertools.chain.from_iterable([c]*qty for c, qty in CHITS.items()))
    random.shuffle(terrain_pile)
    random.shuffle(chit_pile)
    chit_pile.insert(terrain_pile.index(Terrain.Desert), 0)
    for i, j in zip(terrain_pile, chit_pile):
        print(i, j)


if __name__ == '__main__':
    randomize_chits_terrains()
