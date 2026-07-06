from core.race_engine import RaceEngine
from core.finance_engine import FinanceEngine
from ui.dashboard import Dashboard

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
)


class SessionSetup(QWidget):

    def showEvent(self, event):
        print("SessionSetup is visible")
        super().showEvent(event)

    def __init__(self, database, strategies):

        super().__init__()

        self.database = database

        self.setWindowTitle("BetLab - Start Session")

        self.resize(420, 550)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Session Name"))
        self.session_name = QLineEdit("Evening Session")
        layout.addWidget(self.session_name)

        layout.addWidget(QLabel("Strategy"))
        self.strategy = QComboBox()
        self.strategy.addItems(strategies)
        layout.addWidget(self.strategy)

        layout.addWidget(QLabel("Live Race Number"))
        self.live_race = QLineEdit("1")
        layout.addWidget(self.live_race)

        layout.addWidget(QLabel("Current 5× Gap"))
        self.gap = QLineEdit("0")
        layout.addWidget(self.gap)

        layout.addWidget(QLabel("Porsche Drought"))
        self.p = QLineEdit("0")
        layout.addWidget(self.p)

        layout.addWidget(QLabel("Mercedes Drought"))
        self.m = QLineEdit("0")
        layout.addWidget(self.m)

        layout.addWidget(QLabel("McLaren Drought"))
        self.ml = QLineEdit("0")
        layout.addWidget(self.ml)

        layout.addWidget(QLabel("Lamborghini Drought"))
        self.l = QLineEdit("0")
        layout.addWidget(self.l)

        layout.addWidget(QLabel("Starting Bankroll"))
        self.bankroll = QLineEdit("0")
        layout.addWidget(self.bankroll)

        self.start_btn = QPushButton("Start Session")
        self.start_btn.clicked.connect(self.start_session)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)
    
    def start_session(self):

        engine = RaceEngine()

        finance = FinanceEngine(
            int(self.bankroll.text())
        )

        engine.initialize_session(

            int(self.live_race.text()),
            int(self.gap.text()),
            int(self.p.text()),
            int(self.m.text()),
            int(self.ml.text()),
            int(self.l.text())

        )

        session_id = self.database.create_session()

        self.dashboard = Dashboard(
            self.database,
            session_id,
            engine,
            finance
        )

        self.dashboard.show()

        self.close()