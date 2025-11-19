from models.ship import Ship
from utils.enums import ShipType, Team


class ShipFactory:
    def __init__(self, board_view, board_model):
        self.board_view = board_view
        self.board_model = board_model

    def create_ship(self, data: dict, team: Team) -> Ship:
        ship = Ship(
            name=data["name"],
            x=data["initial_x"],
            y=data["initial_y"],
            ship_type=ShipType(data["type"].lower()),
            team=team,
            damage=data["damage"],
            max_hp=data["hp"],
            speed=data["speed"],
        )

        ship_view = self.board_view.draw_ship(data["sprite_path"], ship.x, ship.y)
        ship.view = ship_view
        self.board_model.place_entity(ship, ship.x, ship.y)

        def on_damage(damaged_ship: Ship):
            ship_view.update_hp_bar(damaged_ship.hp / damaged_ship.max_hp)
            if damaged_ship.hp <= 0:
                self.board_view.clear_cell(damaged_ship.x, damaged_ship.y)
                self.board_model.remove_entity(damaged_ship.x, damaged_ship.y)

        ship.on_damage = on_damage
        return ship