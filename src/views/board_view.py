from views.ship_view import ShipView
from abc import ABC, abstractmethod


class BoardView(ABC):

    @abstractmethod
    def draw_ship(self, sprite_path : str, x: int, y: int) -> ShipView:
        pass

    @abstractmethod
    def draw_island(self, sprite_path: str, x: int, y: int):
        pass

    @abstractmethod
    def animate_move(self, old_x: int, old_y: int, new_x: int, new_y: int, on_finished = None):
        pass

    @abstractmethod
    def hover_cell(self, x: int, y: int):
        pass

    @abstractmethod
    def unhover_cell(self, x: int, y: int):
        pass

    @abstractmethod
    def clear_cell(self, x: int, y: int):
        pass