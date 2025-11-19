from enum import Enum


class Team(Enum):
    GREEN = "Royal Navy"
    RED = "Kaiserliche Marine"

class ShipType(Enum):
    DESTROYER = "destroyer"
    CRUISER = "cruiser"
    BATTLESHIP = "battleship"

class IslandType(Enum):
    LOW = "low"      # island.png
    HIGH = "high"    # cliff.png

TEAM_MAPPING = {
    "Royal Navy": Team.GREEN,
    "Kaiserliche Marine": Team.RED,
}

TEAM_DISPLAY_NAME = {v: k for k, v in TEAM_MAPPING.items()}