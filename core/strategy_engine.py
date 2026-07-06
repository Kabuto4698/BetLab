import json
from pathlib import Path


class StrategyEngine:

    def __init__(self):

        Path("strategies").mkdir(exist_ok=True)

        self.strategy_name = "C1"

        self.strategy = {}

        self.load(self.strategy_name)

    def load(self, name):

        filename = Path("strategies") / f"{name}.json"

        if not filename.exists():

            self.strategy = {
                "name": name,
                "rules": []
            }

            return

        with open(filename, "r", encoding="utf-8") as f:
            self.strategy = json.load(f)

        self.strategy_name = name

    def get_recommendation(self, gap, drought):

        for rule in self.strategy["rules"]:

            # ---------- Gap ----------

            if not (rule["gap_min"] <= gap <= rule["gap_max"]):
                continue

            # ---------- Drought ----------

            if "drought" in rule:

                valid = True

                for car, minimum in rule["drought"].items():

                    if drought[car] < minimum:
                        valid = False
                        break

                if not valid:
                    continue

            return rule["bets"]

        return {
            "5": 0,
            "P": 0,
            "M": 0,
            "ML": 0,
            "L": 0
        }

    def available_strategies(self):

        names = []

        for file in Path("strategies").glob("*.json"):
            names.append(file.stem)

        names.sort()

        return names