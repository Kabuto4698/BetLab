from core.conditions import HANDLERS
from core.recommendation import Recommendation


class RuleEngine:

    def evaluate_condition(self, condition, engine):

        handler = HANDLERS.get(
            condition["type"]
        )

        if handler:

            return handler(
                condition,
                engine
            )

        return False

    def evaluate_rule(self, rule, engine):

        results = []

        for condition in rule["conditions"]:

            results.append(
                self.evaluate_condition(
                    condition,
                    engine
                )
            )

        logic = rule.get("logic", "AND")

        if logic == "AND":
            return all(results)

        if logic == "OR":
            return any(results)

        return False

    def get_recommendation(self, strategy, engine):

        recommendation = {

            "5": 0,
            "P": 0,
            "M": 0,
            "ML": 0,
            "L": 0

        }

        triggered_rules = []

        for rule in strategy["rules"]:

            if self.evaluate_rule(rule, engine):

                triggered_rules.append(
                    rule
                )

                for vehicle, amount in rule["bets"].items():

                    recommendation[vehicle] += amount

        return Recommendation(

            bets=recommendation,

            triggered_rules=triggered_rules,

            race_number=engine.race_number,

            gap=engine.current_gap,

            drought=engine.drought.copy()

        )