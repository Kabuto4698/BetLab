print("Dashboard Loaded")

print("Session Setup Loaded")

import config

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)

from PySide6.QtGui import QShortcut, QKeySequence
from core.race_engine import RaceEngine
from core.strategy_engine import StrategyEngine


class Dashboard(QWidget):

    def __init__(
        self,
        database,
        session_id,
        engine,
        finance,
    ):

        super().__init__()

        self.database = database
        self.session_id = session_id

        self.engine = engine
        self.finance = finance
        self.strategy = StrategyEngine()

        self.setWindowTitle("BetLab")
        self.resize(500, 700)

        self.layout = QVBoxLayout()

        self.strategy_dropdown = QComboBox()

        self.strategy_dropdown.addItems(
        self.strategy.available_strategies()
        )

        self.strategy_dropdown.setCurrentText(
        self.strategy.strategy_name
        )

        self.strategy_dropdown.currentTextChanged.connect(
        self.change_strategy
        )

        self.layout.addWidget(self.strategy_dropdown)

        self.title = QLabel("🎰 BetLab")
        self.layout.addWidget(self.title)

        self.race_label = QLabel()
        self.layout.addWidget(self.race_label)

        self.gap_label = QLabel()
        self.layout.addWidget(self.gap_label)

        self.recommendation_label = QLabel()
        self.layout.addWidget(self.recommendation_label)

        self.total_stake_label = QLabel()
        self.layout.addWidget(self.total_stake_label)

        self.balance_label = QLabel()
        self.layout.addWidget(self.balance_label)

        self.session_profit_label = QLabel()
        self.layout.addWidget(self.session_profit_label)

        self.last_result_label = QLabel()
        self.layout.addWidget(self.last_result_label)

        # ---------- HISTORY ----------
        self.history_label = QLabel()
        self.layout.addWidget(self.history_label)

        # ---------- DROUGHTS ----------
        self.p_label = QLabel()
        self.layout.addWidget(self.p_label)

        self.m_label = QLabel()
        self.layout.addWidget(self.m_label)

        self.ml_label = QLabel()
        self.layout.addWidget(self.ml_label)

        self.l_label = QLabel()
        self.layout.addWidget(self.l_label)

        # ---------- BUTTONS ----------
        self.btn5 = QPushButton("⭐ 5×")
        self.btnP = QPushButton("🏎 Porsche")
        self.btnM = QPushButton("🚙 Mercedes")
        self.btnML = QPushButton("🏁 McLaren")
        self.btnL = QPushButton("🟠 Lamborghini")
        self.btnUndo = QPushButton("↩ Undo")

        self.layout.addWidget(self.btn5)
        self.layout.addWidget(self.btnP)
        self.layout.addWidget(self.btnM)
        self.layout.addWidget(self.btnML)
        self.layout.addWidget(self.btnL)
        self.layout.addWidget(self.btnUndo)

        self.btn5.clicked.connect(lambda: self.log("5"))
        self.btnP.clicked.connect(lambda: self.log("P"))
        self.btnM.clicked.connect(lambda: self.log("M"))
        self.btnML.clicked.connect(lambda: self.log("ML"))
        self.btnL.clicked.connect(lambda: self.log("L"))
        self.btnUndo.clicked.connect(self.undo)

        self.setLayout(self.layout)

        # ---------- SHORTCUTS ----------

        QShortcut(QKeySequence("1"), self).activated.connect(
            lambda: self.log("5")
        )

        QShortcut(QKeySequence("2"), self).activated.connect(
            lambda: self.log("P")
        )

        QShortcut(QKeySequence("3"), self).activated.connect(
            lambda: self.log("M")
        )

        QShortcut(QKeySequence("4"), self).activated.connect(
            lambda: self.log("ML")
        )

        QShortcut(QKeySequence("5"), self).activated.connect(
        lambda: self.log("L")
        )

        QShortcut(
            QKeySequence("Ctrl+Z"),
            self
        ).activated.connect(self.undo)

        self.refresh()

    def log(self, winner):

        gap_before = self.engine.current_gap

        recommendation = self.strategy.get_recommendation(
            gap_before,
            self.engine.drought
        )

        self.finance.settle_bet(
            recommendation,
            winner
        )

        self.engine.add_race(winner)

        gap_after = self.engine.current_gap

        self.database.save_race(
            self.session_id,
            winner,
            gap_before,
            gap_after
        )

        self.refresh()
    
    def undo(self):

        races = self.database.get_session_races(
            self.session_id
        )

        if not races:
            return

        self.database.delete_last_race(
            self.session_id
        )

        self.engine.reset()

        races = self.database.get_session_races(
            self.session_id
        )

        for winner in races:
            self.engine.add_race(winner)

        self.refresh()

    def change_strategy(self, strategy_name):

        self.strategy.load(strategy_name)

        self.refresh()
    
    def refresh(self):

        self.race_label.setText(
            f"Race #{self.engine.race_number}"
        )

        self.gap_label.setText(
            f"Current Gap: {self.engine.current_gap}"
        )

        recommendation = self.strategy.get_recommendation(
        self.engine.current_gap,
        self.engine.drought 
        )

        stake = self.finance.total_stake(
            recommendation
        )

        self.total_stake_label.setText(
            f"Total Stake: {stake}"
        )

        self.balance_label.setText(
            f"Balance: {self.finance.current_balance}"
        )   

        self.session_profit_label.setText(
            f"Session P/L: {self.finance.session_profit()}"
        )

        self.last_result_label.setText(
            f"Last Result: {self.finance.last_result}"  
        )

        text = ""

        for bet, amount in recommendation.items():

            if amount > 0:

                text += f"{bet}: {amount}\n"

        if text == "":

            text = "No Bet"

        self.recommendation_label.setText(
            f"Strategy: {self.strategy.strategy_name}\n\n{text}"
        )

        self.p_label.setText(
            f"Porsche Drought: {self.engine.drought['P']}"
        )

        self.m_label.setText(
            f"Mercedes Drought: {self.engine.drought['M']}"
        )

        self.ml_label.setText(
            f"McLaren Drought: {self.engine.drought['ML']}"
        )

        self.l_label.setText(
            f"Lamborghini Drought: {self.engine.drought['L']}"
        )

        # ---------------- History ----------------

        self.history_label.setText(

            "History\n\n"

            + self.engine.history.display(
                config.HISTORY_MODE
            )

        )