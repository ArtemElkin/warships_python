from typing import List, Optional
from core import GameAPI, Image
from views.board_view import BoardView
from views.ship_view_qt import ShipViewQT


class BoardViewQT(BoardView):
    api: GameAPI

    def __init__(self, grid_size: int, api: GameAPI):
        self.api = api
        self.images_grid: List[List[Optional[Image]]] = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    def draw_ship(self, sprite_path : str, x: int, y: int) -> ShipViewQT:
        marker = self.api.addMarker(sprite_path, x, y)
        self.images_grid[x][y] = marker
        return ShipViewQT(marker)

    def draw_island(self, sprite_path: str, x: int, y: int):
        image = self.api.addImage(sprite_path, x, y)
        self.images_grid[x][y] = image

    def animate_move(self, old_x: int, old_y: int, new_x: int, new_y: int, on_finished = None):
        marker = self.images_grid[old_x][old_y]
        if not marker:
            return

        wrapped = MarkerWrapper(marker)
        wrapped.move_to(new_x, new_y, on_finished=on_finished)

        self.images_grid[new_x][new_y] = marker
        self.images_grid[old_x][old_y] = None

    def hover_cell(self, x: int, y: int):
        self.images_grid[x][y].setSelected(True)

    def unhover_cell(self, x: int, y: int):
        self.images_grid[x][y].setSelected(False)

    def clear_cell(self, x: int, y: int):
        self.images_grid[x][y].remove()
        self.images_grid[x][y] = None

class MarkerWrapper:
    def __init__(self, marker):
        self.marker = marker

    def move_to(self, x, y, on_finished=None):
        if on_finished:
            try:
                self.marker.anim.finished.disconnect()
            except TypeError:
                pass
            self.marker.anim.finished.connect(on_finished)
        self.marker.moveTo(x, y)
