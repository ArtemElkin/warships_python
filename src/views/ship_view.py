from abc import ABC, abstractmethod


class ShipView(ABC):
    @abstractmethod
    def update_hp_bar(self, part: float):
        pass
