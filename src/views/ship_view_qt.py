from core import Marker
from views.ship_view import ShipView


class ShipViewQT(ShipView):
    def __init__(self, marker: Marker):
        self.marker = marker

    def update_hp_bar(self, part: float):
        self.marker.setHealth(part)