class StrategyStatistics:

    def __init__(self):

        self.stats = {}

    def create_rule(self, name):

        if name not in self.stats:

            self.stats[name] = {

                "triggers": 0,
                "wins": 0,
                "losses": 0

            }

    def triggered(self, name):

        self.create_rule(name)

        self.stats[name]["triggers"] += 1

    def won(self, name):

        self.create_rule(name)

        self.stats[name]["wins"] += 1

    def lost(self, name):

        self.create_rule(name)

        self.stats[name]["losses"] += 1

    def get(self, name):

        self.create_rule(name)

        return self.stats[name]

    def all(self):

        return self.stats
    
    def win_rate(self, name):

        stat = self.get(name)

        if stat["triggers"] == 0:
            return 0

        return round(
            stat["wins"] / stat["triggers"] * 100,
            2
        )
    
    def summary(self):

        result = {}

        for name, stat in self.stats.items():

            result[name] = {

                **stat,

                "win_rate": self.win_rate(name)

            }

        return result