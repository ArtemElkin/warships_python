from random import randint, choice
from factories.ship_factory import ShipFactory
from models.board_model import BoardModel
from models.player import Player
from models.ship import Ship
from models.island import Island
from utils.logger import logger
from utils.enums import Team, IslandType, TEAM_MAPPING, TEAM_DISPLAY_NAME
from utils.coords import coord_to_label
from utils.manhattan_distance import manhattan_dist
from views.board_view import BoardView
from constants import GRID_SIZE, Sprite


class BoardPresenter:
    board_model: BoardModel
    board_view: BoardView
    selected_ship: Ship
    player1: Player
    player2: Player

    def __init__(self, model: BoardModel, view: BoardView, starting_team: Team):
        self.board_model = model
        self.board_view = view
        self.selected_ship = None
        self.current_team = starting_team
        self.selecting_blocked = False

    def handle_click(self, x: int, y: int) -> None:
        if self.selecting_blocked:
            return
        if self.selected_ship:
            self.board_view.unhover_cell(self.selected_ship.x, self.selected_ship.y)
            if self.board_model.is_empty(x, y):
                self._move_ship(self.selected_ship, x, y)
            self.selected_ship = None
        else:
            ship = self.board_model.get_ship_at(x, y)
            if ship and ship.team == self.current_team:
                self.selected_ship = ship
                self.board_view.hover_cell(ship.x, ship.y)



    def spawn_ships_from_data(self, ships_data: dict, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

        factory = ShipFactory(self.board_view, self.board_model)

        for team_name, ships in ships_data.items():
            try:
                team = TEAM_MAPPING[team_name]
            except ValueError:
                logger.error(f"Unknown team: {team_name}")
                continue

            player = player1 if team == Team.GREEN else player2

            for ship_data in ships:
                try:
                    ship = factory.create_ship(ship_data, team)
                    player.add_ship(ship)
                except Exception as e:
                    logger.error(f"Failed to create ship: {e}")

    def spawn_islands(self, max_count: int = 15):
        placed = 0

        for _ in range(max_count):
            x = randint(0, GRID_SIZE - 1)
            y = randint(0, GRID_SIZE - 1)

            if not self.board_model.is_empty(x, y):
                continue

            island_type = choice([IslandType.LOW, IslandType.HIGH])
            sprite = (
                Sprite.ISLAND
                if island_type == IslandType.LOW
                else Sprite.CLIFF
            )

            island = Island(x, y, island_type)
            if not self.board_model.place_entity(island, x, y):
                continue

            self.board_view.draw_island(sprite, x, y)

            placed += 1

    def _move_ship(self, ship: Ship, new_x: int, new_y: int):
        def on_move_done():
            self.board_model.move_ship(ship, new_x, new_y)
            if self.current_team == Team.GREEN:
                self.player2.attack_enemies(self.board_model)
            elif self.current_team == Team.RED:
                self.player1.attack_enemies(self.board_model)
            self._end_turn()

        dist = manhattan_dist(ship.x, ship.y, new_x, new_y)
        if dist <= ship.speed:
            logger.info(f"{ship.name} moves to  {coord_to_label(new_x, new_y)}")
            self.board_view.animate_move(ship.x, ship.y, new_x, new_y, on_move_done)

    def _check_wins(self) -> bool:
        """Проверяет победу и выводит красивое сообщение."""
        if not self.player1.alive_ships():
            winner = Team.RED
            loser = Team.GREEN
        elif not self.player2.alive_ships():
            winner = Team.GREEN
            loser = Team.RED
        else:
            return False

        winner_name = TEAM_DISPLAY_NAME[winner]
        loser_name = TEAM_DISPLAY_NAME[loser]

        logger.info("\n" + "=" * 35)
        logger.info(f"    {winner_name.upper()} WINS!".center(35))
        logger.info(f"All {loser_name} ships have been destroyed.")
        logger.info("=" * 35 + "\n")

        self.selecting_blocked = True
        return True

    def _end_turn(self):
        self.current_team = Team.RED if self.current_team == Team.GREEN else Team.GREEN

        if self._check_wins():
            return

        current_name = TEAM_DISPLAY_NAME[self.current_team]
        logger.info(f"-- -- {current_name} -- --")
