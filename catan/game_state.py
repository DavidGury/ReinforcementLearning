from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from catan_objects import Request, Event
from condition import Condition
from typing import Protocol, Callable
from abc import ABC, abstractmethod


@dataclass
class GameContext(Protocol):
    _state: GameState

    def set_state(self, state: GameState):
        ...


@dataclass
class GameState(ABC):
    """
    Handles requests (action inputs) for game
    Allows mapping custom functions/methods to handle requests in different ways for various game states
    """
    _context: GameContext = field(default=None, repr=False)

    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, context: GameContext) -> None:
        self._context = context

    def handle_request(self, request: Request, *args) -> None:
        """ Looks up which function/method to call for given request
        in _request_handling and passes arguments to that function """
        func = self.request_functions[request]
        func(self.context, *args)

    def handle_undefined_request(self) -> None:
        return

    @property
    @abstractmethod
    def request_functions(self) -> dict[Request, Callable[[GameContext, ...], None]]:
        ...


@dataclass
class StateMap(dict):
    data: InitVar[dict[Event, GameState]]
    _state_map: dict[int, GameState] = field(default_factory=dict)

    def __post_init__(self, data: dict[Event, GameState]):
        for event, state in data.items():
            self.register(event.value, state)

    @property
    def state_map(self) -> dict[int, GameState]:
        return self._state_map.copy()

    def register(self, event: Event, state: GameState):
        self._state_map[event.value] = state
