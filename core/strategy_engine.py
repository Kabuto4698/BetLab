import json
from pathlib import Path
from core.rule_engine import RuleEngine


class StrategyEngine:

    def __init__(self):

        Path("strategies").mkdir(exist_ok=True)

        self.strategy_name = "C1"

        self.strategy = {}

        self.rule_engine = RuleEngine()

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

    def get_recommendation(self, engine):

        return self.rule_engine.get_recommendation(
            self.strategy,
            engine
        )

    def available_strategies(self):

        names = []

        for file in Path("strategies").glob("*.json"):
            names.append(file.stem)

        names.sort()

        return names