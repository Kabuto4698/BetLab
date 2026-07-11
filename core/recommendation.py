class Recommendation:

    def __init__(
        self,
        bets=None,
        triggered_rules=None,
        race_number=0,
        gap=0,
        drought=None
    ):

        self.bets = bets or {

            "5": 0,
            "P": 0,
            "M": 0,
            "ML": 0,
            "L": 0

        }

        self.triggered_rules = triggered_rules or []

        self.race_number = race_number

        self.gap = gap

        self.drought = drought or {}