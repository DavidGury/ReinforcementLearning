from dataclasses import dataclass, field, InitVar
from catan_objects import *
import numpy as np
import numpy.typing as npt
from typing import Protocol


DEFAULT_SPACE = Space.Null
DEFAULT_ENV = Environment.Sea
ROBBER_START = Terrain.Desert


class TileInfo(Protocol):
    space: Space
    env: Environment
    object: CatanBoardObject
    chit_value: int
    connections: list[int]


@dataclass
class BoardData:
    tile_data: InitVar[list[TileInfo]]
    n_tiles: int = field(init=False)
    space: npt.NDArray[Space] = field(init=False)
    environment: npt.NDArray[Environment] = field(init=False)
    objects: npt.NDArray[CatanBoardObject] = field(init=False)
    owner: npt.NDArray[np.uint8] = field(init=False)
    chit: npt.NDArray[np.uint8] = field(init=False)
    connections: npt.NDArray[np.uint8] = field(init=False)
    build_dists: npt.NDArray[np.uint8] = field(init=False)
    robber: int = 0
    last_placement: int = 0

    def __post_init__(self, tile_data: list[TileInfo]):
        self.n_tiles = len(tile_data)
        self.space, self.environment, self.objects, self.chit = np.array(
            [[tile.space, tile.env, tile.object, tile.chit_value] for tile in tile_data],
            dtype=np.uint8
        ).T
        self.owner = np.full((self.n_tiles,), -1, dtype=np.uint8)
        self.connections = np.array(fill_connections([tile.connections for tile in tile_data]), dtype=np.uint8)

    def package_observation(self, cur_player: int) -> dict[str, npt.NDArray[np.uint8]]:
        return {
            # 'board_spaces': self.space,
            # 'board_environments': self.environment,
            'board_objects': self.objects,
            'board_owners': self.owner,
            'board_chits': self.chit,
            'board_robber': np.array([self.robber], dtype=np.uint8),
            'board_last': np.array([self.last_placement], dtype=np.uint8),
        }


def fill_connections(connection_list: list[list[int]]) -> list[list[int]]:
    """ Makes sublist lengths uniform so they can be converted to array """
    w = max(map(len, connection_list))
    for y in range(len(connection_list)):
        n_missing = w - len(connection_list[y])
        connection_list[y].extend([connection_list[y][-1]] * n_missing)
    return connection_list
