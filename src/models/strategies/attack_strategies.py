from typing import List
from abc import ABC, abstractmethod
from models.board_model import BoardModel
from models.island import Island
from models.ship import Ship
from utils.enums import IslandType


class AttackStrategy(ABC):
    @abstractmethod
    def find_targets(self, attacker: Ship, board_model: BoardModel) -> List[Ship]:
        """Возвращает список целей для атаки"""
        pass


class DestroyerAttackStrategy(AttackStrategy):
    def find_targets(self, attacker: Ship, board_model: BoardModel) -> List[Ship]:
        targets = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ship_to_check = board_model.get_ship_at(attacker.x + x, attacker.y + y)
                if ship_to_check and ship_to_check.team != attacker.team:
                    targets.append(ship_to_check)
        return targets


class CruiserBattleshipAttackStrategy(AttackStrategy):
    def find_targets(self, attacker: Ship, board_model: BoardModel) -> List[Ship]:
        targets = []

        targets.extend(self._raycast_line(attacker, board_model, dx=1, dy=0))
        targets.extend(self._raycast_line(attacker, board_model, dx=-1, dy=0))

        targets.extend(self._raycast_line(attacker, board_model, dx=0, dy=1))
        targets.extend(self._raycast_line(attacker, board_model, dx=0, dy=-1))

        return targets

    def _raycast_line(self, attacker: Ship, board_model: BoardModel, dx: int, dy: int) -> List[Ship]:
        targets = []
        x, y = attacker.x + dx, attacker.y + dy

        while 0 <= x < 7 and 0 <= y < 7:
            entity = board_model.get_entity_at(x, y)
            if isinstance(entity, Island):
                island = entity
                if island.type == IslandType.HIGH:
                    break
            elif isinstance(entity, Ship):
                enemy = entity
                if enemy.team != attacker.team:
                    targets.append(enemy)

            x += dx
            y += dy

        return targets