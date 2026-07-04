import sys

from PySide6.QtWidgets import QApplication

from ui.dashboard import Dashboard
from core.database import Database


def main():

    db = Database()

    app = QApplication(sys.argv)

    window = Dashboard(db)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()