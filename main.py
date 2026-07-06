import sys

from PySide6.QtWidgets import QApplication

from core.database import Database
from core.strategy_engine import StrategyEngine

from ui.session_setup import SessionSetup

def main():

    app = QApplication(sys.argv)

    db = Database()

    strategy_engine = StrategyEngine()

    session_setup = SessionSetup(
    db,
    strategy_engine.available_strategies()
    )

    session_setup.show()

    print("Showing Session Setup...")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()