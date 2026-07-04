class StrategyEngine:

    def __init__(self):
        self.current_strategy = "C1"

    def get_recommendation(self, gap):

        if self.current_strategy == "C1":

            if gap <= 3:
                return "NO BET"

            elif gap <= 7:
                return (
                    "Porsche 60\n"
                    "Mercedes 40\n"
                    "McLaren 20\n"
                    "Lamborghini 20"
                )

            else:
                return "5× 100"

        return "NO STRATEGY"