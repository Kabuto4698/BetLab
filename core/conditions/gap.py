def evaluate(condition, engine):

    minimum = condition.get("min", 0)
    maximum = condition.get("max", 999999)

    return minimum <= engine.current_gap <= maximum