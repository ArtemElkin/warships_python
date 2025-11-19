import json
import os
from typing import Dict, Any

class ShipDataLoader:
    @staticmethod
    def load(path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Ships data not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

ship_data_loader = ShipDataLoader()