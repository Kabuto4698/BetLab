from core.history import History


class RaceEngine:

    def __init__(self):

        self.history = History()

        self.reset()

    def reset(
        self,
        live_race=1,
        gap=0,
        p=0,
        m=0,
        ml=0,
        l=0,
    ):

        self.live_race = live_race

        self.race_number = 1

        self.current_gap = gap

        self.drought = {
        "P": p,
        "M": m,
        "ML": ml,
        "L": l
        }

        self.history.clear()

    def initialize_session(
        self,
        live_race,
        gap,
        p,
        m,
        ml,
        l,
    ):

        self.reset(
        live_race,
        gap,
        p,
        m,
        ml,
        l,
    )

    def add_race(self, winner):

        self.history.add(winner)

        self.race_number += 1

        if winner == "5":

            self.current_gap += 1

            self.drought["P"] += 1
            self.drought["M"] += 1
            self.drought["ML"] += 1
            self.drought["L"] += 1

        else:

            self.current_gap = 0

            for car in self.drought:

                if car == winner:
                    self.drought[car] = 0
                else:
                    self.drought[car] += 1