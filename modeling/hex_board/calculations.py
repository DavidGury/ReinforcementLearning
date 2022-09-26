from .tiles import TileType


def calc_hex_height(pixel_height: int, n_hexes_yaxis: int) -> int:
    n_eighths = n_hexes_yaxis * 6 + 2
    return pixel_height // n_eighths * 8


def calc_hex_width(pixel_width: int, n_hexes_xaxis: int) -> int:
    n_eighths = n_hexes_xaxis * 8 + 4
    return pixel_width // n_eighths * 8


def calc_buffer_width(pixel_width: int, hex_width: int, n_hexes_xaxis: int) -> int:
    total_hex_pixel_width = (hex_width * (2 * n_hexes_xaxis + 1)) / 2
    return int((pixel_width - total_hex_pixel_width) / 2)


def calc_buffer_height(pixel_height: int, hex_height: int, n_hexes_yaxis: int) -> int:
    total_hex_pixel_height = (hex_height * (n_hexes_yaxis * 3 + 1)) / 4
    return int((pixel_height - total_hex_pixel_height) / 2)


def calc_display_area(n_pixels: int, margin: int, divisor_req: int) -> int:
    """
    Finds the highest pixel count that meets the following requirements:
        -is evenly divisible by provided divisor integer
        -will not overlap margins
    """
    area_inside_margin = int(n_pixels * (margin / 100))
    return area_inside_margin // divisor_req * divisor_req


def get_path_type(conn_1: tuple[int, int], conn_2: tuple[int, int]) -> TileType:
    conn_y1, conn_x1 = conn_1
    conn_y2, conn_x2 = conn_2
    if conn_x1 == conn_x2:
        return TileType.PathVertical
    elif (conn_y1 > conn_y2) == (conn_x1 > conn_x2):
        return TileType.PathSlopedL
    return TileType.PathSlopedR
