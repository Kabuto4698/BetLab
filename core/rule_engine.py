from core.conditions import HANDLERS


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

        for rule in strategy["rules"]:

            if self.evaluate_rule(rule, engine):

                for vehicle, amount in rule["bets"].items():

                    recommendation[vehicle] += amount

        return recommendation