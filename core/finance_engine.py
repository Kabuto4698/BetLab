import json
from pathlib import Path

class FinanceEngine:

    def __init__(self, starting_balance):

        self.starting_balance = starting_balance

        self.current_balance = starting_balance

        self.last_result = 0

        with open(
            Path("config") / "vehicles.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.vehicles = json.load(f)

    def total_stake(self, recommendation):

        total = 0

        for vehicle, amount in recommendation.items():

            count = self.vehicles[vehicle]["count"]

            total += amount * count

        return total

    def settle_bet(self, recommendation, winner):

        stake = self.total_stake(recommendation)

        payout = 0

        if winner in recommendation:

            multiplier = self.vehicles[winner]["multiplier"]

            payout = recommendation[winner] * multiplier

        profit = payout - stake

        self.current_balance += profit

        self.last_result = profit

        return profit

    def session_profit(self):

        return self.current_balance - self.starting_balance