from __future__ import annotations
from dataclasses import dataclass, field
from condition import ConditionKeeper
from .board import BoardData
from .building_data import BuildingData
from .development import DevelopmentData
from .event import EventData
from .resources import ResourceData
from .status import StatusData
from .trade import TradeData
import numpy as np
import numpy.typing as npt


@dataclass
class GameData(ConditionKeeper):
    status: StatusData
    event: EventData
    resources: ResourceData
    development: DevelopmentData
    trade: TradeData
    board: BoardData
    buildings: BuildingData

    def package_observation(self) -> dict[str, npt.NDArray[np.uint8]]:
        cur_player = self.status.cur_player
        return {
            **self.status.package_observation(),
            **self.event.package_observation(),
            **self.resources.package_observation(cur_player),
            **self.trade.package_observation(cur_player),
            **self.development.package_observation(cur_player),
            **self.board.package_observation(cur_player)
        }
