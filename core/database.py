import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("data").mkdir(exist_ok=True)

        self.connection = sqlite3.connect("data/betlab.db")

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS races(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            winner TEXT NOT NULL,

            gap_before INTEGER,

            gap_after INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.connection.commit()

    def save_race(self, winner, gap_before, gap_after):

        self.cursor.execute(
            """
            INSERT INTO races(
                winner,
                gap_before,
                gap_after
            )
            VALUES(?,?,?)
            """,
            (
                winner,
                gap_before,
                gap_after,
            ),
        )

        self.connection.commit()