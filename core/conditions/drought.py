def evaluate(condition, engine):

    target = condition["target"]

    minimum = condition["min"]

    return engine.drought.get(target, 0) >= minimum