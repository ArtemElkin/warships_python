from typing import List
from models.board_model import BoardModel
from models.strategies.attack_strategies import DestroyerAttackStrategy, CruiserBattleshipAttackStrategy, AttackStrategy
from models.ship import Ship
from utils.enums import Team, ShipType
from utils.manhattan_distance import manhattan_dist


class Player:
    def __init__(self, team: Team):
        self.team = team
        self.ships: List[Ship] = []

    def add_ship(self, ship: Ship) -> None:
        ship.attack_strategy = self._create_strategy(ship.type)
        self.ships.append(ship)

    def alive_ships(self) -> List[Ship]:
        return [s for s in self.ships if s.is_alive()]

    def attack_enemies(self, board_model: BoardModel) -> None:
        for attacker in self.alive_ships():
            targets = attacker.attack_strategy.find_targets(attacker, board_model)
            if not targets:
                continue
            damage_per = attacker.damage // len(targets)
            for target in targets:
                dist = manhattan_dist(attacker.x, attacker.y, target.x, target.y)
                target.take_damage(damage_per, dist, attacker.name)

    def _create_strategy(self, ship_type: ShipType) -> AttackStrategy:
        if ship_type == ShipType.DESTROYER:
            return DestroyerAttackStrategy()
        else:
            return CruiserBattleshipAttackStrategy()