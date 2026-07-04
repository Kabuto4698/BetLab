class RaceEngine:

    def __init__(self):
        self.reset()

    def reset(self):
        self.race_number = 1
        self.current_gap = 0

        self.drought = {
            "P": 0,
            "M": 0,
            "ML": 0,
            "L": 0,
        }

    def add_race(self, winner):

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