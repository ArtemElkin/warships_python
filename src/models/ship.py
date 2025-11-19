from utils.enums import ShipType, Team
from utils.logger import logger


class Ship:
    def __init__(self, name: str, x: int, y: int, ship_type: ShipType, team: Team,
                 damage: int, max_hp: int, speed: int):
        self.name = name
        self.x = x
        self.y = y
        self.type = ship_type
        self.team = team
        self.damage = damage
        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed

        self.on_damage = None

    def take_damage(self, amount: int, attack_distance: int, attacker_name: str) -> None:
        if amount <= 0:
            return
        amount = self._calculate_incoming_damage(amount, attack_distance)
        self.hp -= amount
        if amount != 0:
            logger.info(f"{attacker_name} attacks {self.name} for {amount} damage")
        else:
            logger.info(f"{self.name} blocks all damage from {attacker_name}")
        if self.hp <= 0:
            logger.info(f"{self.name} is sunk!")
        self.on_damage(self)

    def is_alive(self) -> bool:
        return self.hp > 0

    def _calculate_incoming_damage(self, base_damage: int, dist: int) -> int:
        damage = base_damage
        if self.type in [ShipType.CRUISER, ShipType.DESTROYER] and dist > 2:
            damage //= 2
        elif self.type == ShipType.BATTLESHIP and damage <= 10:
            damage = 0
        return min(self.hp, damage)
