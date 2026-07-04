from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from core.race_engine import RaceEngine
from core.strategy_engine import StrategyEngine


class Dashboard(QWidget):

    def __init__(self, database):

        super().__init__()
    
        self.database = database

        self.engine = RaceEngine()

        self.strategy = StrategyEngine()

        self.setWindowTitle("BetLab")

        self.resize(450, 600)

        self.layout = QVBoxLayout()

        self.title = QLabel("🎰 BetLab")
        self.layout.addWidget(self.title)

        self.race_label = QLabel()
        self.layout.addWidget(self.race_label)

        self.gap_label = QLabel()
        self.layout.addWidget(self.gap_label)

        self.recommendation_label = QLabel()
        self.layout.addWidget(self.recommendation_label)

        self.p_label = QLabel()
        self.layout.addWidget(self.p_label)

        self.m_label = QLabel()
        self.layout.addWidget(self.m_label)

        self.ml_label = QLabel()
        self.layout.addWidget(self.ml_label)

        self.l_label = QLabel()
        self.layout.addWidget(self.l_label)

        self.btn5 = QPushButton("⭐ 5×")
        self.btnP = QPushButton("🏎 Porsche")
        self.btnM = QPushButton("🚙 Mercedes")
        self.btnML = QPushButton("🏁 McLaren")
        self.btnL = QPushButton("🟠 Lamborghini")

        self.layout.addWidget(self.btn5)
        self.layout.addWidget(self.btnP)
        self.layout.addWidget(self.btnM)
        self.layout.addWidget(self.btnML)
        self.layout.addWidget(self.btnL)

        self.btn5.clicked.connect(lambda: self.log("5"))
        self.btnP.clicked.connect(lambda: self.log("P"))
        self.btnM.clicked.connect(lambda: self.log("M"))
        self.btnML.clicked.connect(lambda: self.log("ML"))
        self.btnL.clicked.connect(lambda: self.log("L"))

        self.setLayout(self.layout)

        self.refresh()

    def log(self, winner):

        gap_before = self.engine.current_gap

        self.engine.add_race(winner)

        gap_after = self.engine.current_gap

        self.database.save_race(
            winner,
            gap_before,
            gap_after
        )

        self.refresh()

    def refresh(self):

        self.race_label.setText(f"Race #{self.engine.race_number}")

        self.gap_label.setText(
            f"Current Gap: {self.engine.current_gap}"
        )

        recommendation = self.strategy.get_recommendation(
            self.engine.current_gap
        )

        self.recommendation_label.setText(
            f"Recommendation:\n\n{recommendation}"
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