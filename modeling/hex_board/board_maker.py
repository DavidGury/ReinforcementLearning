from dataclasses import dataclass, field, InitVar
from collections import defaultdict
from .tiles import TileInfo, TileType
from . import calculations as calcs


@dataclass
class HexBoard:
    resolution: tuple[int, int]
    n_hexes_yaxis: InitVar[int]
    n_hexes_xaxis: InitVar[int]
    margin: InitVar[int]  # percentage (0-100)
    tiles: list[TileInfo] = field(default_factory=list, repr=True)

    def __post_init__(self, n_hexes_yaxis: int, n_hexes_xaxis: int, margin: int):
        self.validate_margin(margin)
        self.validate_resolution(self.resolution)

        hex_size = min(
            calcs.calc_hex_height(self.resolution[1], n_hexes_yaxis),
            calcs.calc_hex_width(self.resolution[0], n_hexes_xaxis)
        )

        top_buffer = calcs.calc_buffer_height(self.resolution[1], hex_size, n_hexes_yaxis)
        left_buffer = calcs.calc_buffer_width(self.resolution[0], hex_size, n_hexes_xaxis)

        # Populate board tile positions/relationships
        hex_connections, isec_connections, path_connections = defaultdict(set), defaultdict(set), defaultdict(set)

        hex_y = top_buffer + hex_size//2
        for row in range(n_hexes_yaxis):
            ylocs = [hex_y - hex_size//2 + step * hex_size // 8 for step in range(9)]
            hex_x = left_buffer + hex_size//2 + (hex_y % 2) * hex_size//2
            for column in range(n_hexes_xaxis):
                hex_loc = (hex_y, hex_x)
                xlocs = [hex_x + - hex_size//2 + step * hex_size // 4 for step in range(5)]
                isecs = [(ylocs[iy], xlocs[ix]) for (iy, ix) in [(0, 2), (2, 4), (6, 4), (8, 2), (6, 0), (2, 0)]]
                paths = [(ylocs[iy], xlocs[ix]) for (iy, ix) in [(1, 1), (1, 3), (4, 4), (7, 3), (7, 1), (4, 0)]]

                for i in range(6):
                    hex_connections[hex_loc].add(isecs[i])
                    isec_connections[isecs[i]] |= {paths[i], paths[(i+1) % 6], hex_loc}
                    path_connections[paths[i]] = {isecs[i], isecs[i-1]}

                hex_x += hex_size
            hex_y += hex_size * 3 // 4

        conn_tables = [hex_connections, isec_connections, path_connections]
        tile_index = [loc for conn_table in map(sorted, conn_tables) for loc in conn_table]
        tile_connections = {**hex_connections, **isec_connections, **path_connections}

        for i, tile_loc in enumerate(tile_index):
            tile_type = \
                TileType.Hex if tile_loc in hex_connections else \
                TileType.Intersection if tile_loc in isec_connections else \
                calcs.get_path_type(*path_connections[tile_loc])

            self.tiles.append(
                TileInfo(
                    index=i,
                    tile_type=tile_type,
                    loc=tile_loc,
                    connections=tuple(tile_index.index(conn) for conn in tile_connections[tile_loc])
                )
            )

    @staticmethod
    def validate_resolution(resolution: tuple[int, int]) -> None:
        for res_val in resolution:
            if res_val == 0 or res_val % 8:
                raise ValueError('HexBoard attribute \"resolution\" values must be >0 and multiple of 8.')

    @staticmethod
    def validate_margin(margin: int) -> None:
        if not 0 <= margin <= 50:
            raise ValueError('HexBoard attribute \"margin\" must be integer between 0 and 50.')


if __name__ == '__main__':
    ...
