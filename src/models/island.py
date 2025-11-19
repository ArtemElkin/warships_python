from utils.enums import IslandType

class Island:
    def __init__(self, x: int, y: int, island_type: IslandType):
        self.x = x
        self.y = y
        self.type = island_type
