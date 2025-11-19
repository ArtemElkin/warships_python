from typing import List, Optional
from models.ship import Ship
from models.island import Island
from constants import GRID_SIZE


class BoardModel:

    def __init__(self):
        self._reset_()

    def place_entity(self, entity: Ship | Island, x: int, y: int) -> bool:
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return False
        if self.grid[x][y] is not None:
            return False
        self.grid[x][y] = entity
        entity.x, entity.y = x, y
        return True

    def remove_entity(self, x, y):
        self.grid[x][y] = None

    def move_ship(self, ship: Ship, new_x: int, new_y: int) -> bool:
        old_x, old_y = ship.x, ship.y
        if not self.is_empty(new_x, new_y):
            return False
        self.remove_entity(old_x, old_y)
        placed = self.place_entity(ship, new_x, new_y)
        return placed

    def get_ship_at(self, x: int, y: int) -> Optional[Ship]:
        entity = self.get_entity_at(x, y)
        return entity if isinstance(entity, Ship) else None

    def get_island_at(self, x: int, y: int) -> Optional[Island]:
        entity = self.get_entity_at(x, y)
        return entity if isinstance(entity, Island) else None

    def get_entity_at(self, x: int, y: int):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return None
        entity = self.grid[x][y]
        return entity

    def is_empty(self, x: int, y: int) -> bool:
        return self.get_entity_at(x, y) is None

    def _reset_(self):
        self.grid: List[List[Optional[Ship | Island]]] = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
