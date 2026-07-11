import json
from pathlib import Path
from core.rule_engine import RuleEngine
from core.strategy_statistics import StrategyStatistics


class StrategyEngine:

    def __init__(self):

        Path("strategies").mkdir(exist_ok=True)

        self.rule_engine = RuleEngine()

        self.statistics = StrategyStatistics()

        self.last_recommendation = None
        
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

    def generate_recommendation(self, engine):

        recommendation = self.rule_engine.get_recommendation(
            self.strategy,
            engine
        )

        self.last_recommendation = recommendation

        print("Generated:", recommendation.bets)

        print("Triggered:",
            [rule["name"] for rule in recommendation.triggered_rules])

        for rule in recommendation.triggered_rules:

            self.statistics.triggered(
                rule["name"]
            )

        return recommendation
    
    def current_recommendation(self):

        return self.last_recommendation

    def available_strategies(self):

        names = []

        for file in Path("strategies").glob("*.json"):
            names.append(file.stem)

        names.sort()

        return names
    
    def settle_rules(self, winner):

        if self.last_recommendation is None:
            return

        for rule in self.last_recommendation.triggered_rules:

            if winner in rule["bets"]:

                self.statistics.won(
                    rule["name"]
                )

            else:

                self.statistics.lost(
                    rule["name"]
                )

    def save_statistics(self, database):

        for rule_name, stat in self.statistics.all().items():

            database.save_strategy_statistic(

                self.strategy_name,

                rule_name,

                stat["triggers"],

                stat["wins"],

                stat["losses"]

            )