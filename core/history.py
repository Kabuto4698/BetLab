class History:

    def __init__(self):

        self.results = []

    def add(self, winner):

        self.results.append(winner)

        if len(self.results) > 30:
            self.results.pop(0)

    def clear(self):

        self.results.clear()

    def numbers(self):

        return " ".join(self.results)

    def icons(self):

        icons = {
            "5": "⭐",
            "P": "🏎",
            "M": "🚙",
            "ML": "🏁",
            "L": "🟠",
        }

        return " ".join(
            icons.get(race, "?")
            for race in self.results
        )

    def display(self, mode):

        if mode == "numbers":
            return self.numbers()

        if mode == "icons":
            return self.icons()

        return self.numbers() + "\n\n" + self.icons()