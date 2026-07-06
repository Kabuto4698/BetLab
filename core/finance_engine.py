class FinanceEngine:

    def __init__(self, starting_balance):

        self.starting_balance = starting_balance

        self.current_balance = starting_balance

        self.last_result = 0

    def total_stake(self, recommendation):

        return sum(recommendation.values())

    def settle_bet(self, recommendation, winner):

        stake = self.total_stake(recommendation)

        payout = 0

        multipliers = {
            "5": 5,
            "P": 10,
            "M": 15,
            "ML": 25,
            "L": 45,
        }

        if winner in recommendation:

            payout = recommendation[winner] * multipliers[winner]

        profit = payout - stake

        self.current_balance += profit

        self.last_result = profit

        return profit

    def session_profit(self):

        return self.current_balance - self.starting_balance