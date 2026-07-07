from core.conditions import gap
from core.conditions import drought


class RuleEngine:

    def evaluate_condition(self, condition, engine):

        condition_type = condition["type"]

        if condition_type == "gap":
            return gap.evaluate(condition, engine)

        if condition_type == "drought":
            return drought.evaluate(condition, engine)

        return False