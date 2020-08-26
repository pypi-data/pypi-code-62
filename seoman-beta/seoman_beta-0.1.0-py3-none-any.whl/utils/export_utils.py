import json
import csv
from typing import Optional, Dict, Any, Union

# TODO DEBUG
class ExportCSV:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self.data = data

    def export_to_csv(self, filename: Optional[str] = "analytics.csv") -> None:
        with open(filename, "w") as file:
            pass


class ExportJSON:
    def __init__(self, data: Dict[Any, Any] = {}) -> None:
        self.data = data

    def export_to_json(self, filename: Optional[str] = "analytics.json") -> None:
        with open(filename, "w") as file:
            json.dump(self.data, file, indent=4)

        print(f"Analytics successfully created in JSON format ✅")


class ExportTable:
    def __init__(self, data: Dict[Any, Any]):
        self.data = data

    def export_to_table(self):
        pass

