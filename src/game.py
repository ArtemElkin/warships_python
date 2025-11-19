import json
import os
import traceback

from constants import GRID_SIZE
from core import GameAPI
from models.player import Player
from models.board_model import BoardModel
from presenters.board_presenter import BoardPresenter
from views.board_view import BoardView
from views.board_view_qt import BoardViewQT
from utils.enums import Team, TEAM_DISPLAY_NAME
from utils.logger import logger
from services.ships_data_loader import ship_data_loader


def load_ships_from_json(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class Game:
    api: GameAPI
    board_model: BoardModel
    board_presenter: BoardPresenter
    board_view: BoardView
    player1: Player
    player2: Player

    def start(self, api: GameAPI) -> None:
        self.api = api
        logger.bind(api)
        logger.info("Game started")
        starting_team = Team.GREEN
        logger.info(f"-- -- {TEAM_DISPLAY_NAME[starting_team]} -- --")
        self.board_view = BoardViewQT(GRID_SIZE, self.api)
        self.board_model = BoardModel()
        self.board_presenter = BoardPresenter(self.board_model, self.board_view, starting_team)

        self.player1 = Player(Team.GREEN)
        self.player2 = Player(Team.RED)

        try:
            base = os.path.dirname(__file__)
            path = os.path.join(base, "data", "ships_data.json")
            ships_data = ship_data_loader.load(path)
            self.board_presenter.spawn_ships_from_data(ships_data, self.player1, self.player2)
            self.board_presenter.spawn_islands(15)
        except Exception as e:
            logger.error(f"Failed to load ships JSON: {e}")
            logger.info(traceback.format_exc())
            self.ships_data = {}
            return

    def click(self, api: GameAPI, x: int, y: int) -> None:
        self.board_presenter.handle_click(x, y)
