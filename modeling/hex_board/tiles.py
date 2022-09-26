from dataclasses import dataclass, field, InitVar
from enum import Enum, auto
from PIL import Image
import numpy as np
import numpy.typing as npt

COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (192, 192, 192)


class TileType(Enum):
    Hex = 0
    Intersection = 1
    PathVertical = 2  # |
    PathSlopedR = 3   # /
    PathSlopedL = 4   # \


@dataclass(order=True)
class TileInfo:
    index: int = field(compare=True)
    tile_type: TileType
    loc: tuple[int, int]
    connections: tuple[int] = field(default_factory=list)


@dataclass
class TileImage:
    img_path: InitVar[str]
    image: npt.NDArray[np.uint8] = field(init=False)
    _recolor_key: tuple[int, int, int] = field(default=COLOR_GRAY)
    _transparency_key: tuple[int, int, int] = field(default=COLOR_WHITE)

    def __post_init__(self, img_path: str):
        self.image = np.array(Image.open(img_path))
        print(self.image.shape)

    def recolor(self, color: tuple[int, int, int]) -> npt.NDArray[np.uint8]:
        change_locs = np.where(np.all(self.image == self._recolor_key, axis=-1))
        self.image[change_locs] = color
        return self.image


if __name__ == '__main__':
    ...
