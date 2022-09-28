from dataclasses import dataclass, field, InitVar
from catan_objects import *
import numpy as np
import numpy.typing as npt
from typing import Protocol


@dataclass
class BuildingInfo(Protocol):
    building: Building
    space_req: Space
    env_req: list[Environment]
    building_req: Building
    resource_cost: dict[Resource, int]
    build_limit: int
    resource_yield: int


@dataclass
class BuildingData:
    # n_players: InitVar[int]  # TODO - remove with qty built
    building_data: InitVar[list[BuildingInfo]]

    buildings: npt.NDArray[Building] = field(init=False)
    space_reqs: npt.NDArray[Space] = field(init=False)
    environment_reqs: npt.NDArray[bool] = field(init=False)
    building_reqs: npt.NDArray[Building] = field(init=False)
    costs: npt.NDArray[np.uint8] = field(init=False)
    build_limits: npt.NDArray[np.uint8] = field(init=False)
    yield_qtys: npt.NDArray[np.uint8] = field(init=False)
    # qty_built: npt.NDArray[np.uint8] = field(init=False)  # TODO - move to board
    n_buildings: int = field(init=False)

    def __post_init__(self, building_data: list[BuildingInfo]):
        self.n_buildings = len(building_data)
        self.buildings, self.space_reqs, self.building_reqs, self.build_limits, self.yield_qtys = [
            np.array(
                [object.__getattribute__(b, attr) for b in building_data],
                dtype=np.dtype(data_type)
            )
            for attr, data_type in [
                ('building', Building),
                ('space_req', Space),
                ('building_req', Building),
                ('build_limit', np.uint8),
                ('resource_yield', np.uint8)
            ]
        ]

        self.costs = np.array(
            [
                [0 if res not in b.resource_cost else b.resource_cost[res] for res in Resource]
                for b in building_data
            ],
            dtype=np.uint8
        )

        self.environment_reqs = np.array(
            [
                [env in b.env_req for env in Environment]
                for b in building_data
            ],
            dtype=bool
        )

    def package_observation(self) -> dict[str, npt.NDArray[np.uint8]]:
        return {
            'space_reqs': self.space_reqs,
            'environment_reqs': self.environment_reqs,
            'building_reqs': self.building_reqs,
            'costs': self.costs.ravel(),
            'build_limits': self.build_limits,
            'yield_qtys': self.yield_qtys,
            # 'qty_built': self.qty_built.ravel(),  # TODO - remove
        }

