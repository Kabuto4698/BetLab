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
        CREATE TABLE IF NOT EXISTS sessions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            ended_at TIMESTAMP,

            starting_bankroll INTEGER DEFAULT 0,

            ending_bankroll INTEGER DEFAULT 0,

            profit INTEGER DEFAULT 0

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS races(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id INTEGER,

            winner TEXT,

            gap_before INTEGER,

            gap_after INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(session_id) REFERENCES sessions(id)

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy_statistics(

            strategy_name TEXT,

            rule_name TEXT,

            triggers INTEGER DEFAULT 0,

            wins INTEGER DEFAULT 0,

            losses INTEGER DEFAULT 0,

            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            
            PRIMARY KEY (
                strategy_name,
                rule_name
            )

        )
        """)                   

        self.connection.commit()

    def create_session(self):

        self.cursor.execute("""
        INSERT INTO sessions(starting_bankroll)
        VALUES(0)
        """)

        self.connection.commit()

        return self.cursor.lastrowid

    def save_race(
        self,
        session_id,
        winner,
        gap_before,
        gap_after,
    ):

        self.cursor.execute(
            """
            INSERT INTO races(
                session_id,
                winner,
                gap_before,
                gap_after
            )
            VALUES(?,?,?,?)
            """,
            (
                session_id,
                winner,
                gap_before,
                gap_after,
            ),
        )

        self.connection.commit()

    def get_session_races(self, session_id):

        self.cursor.execute(
            """
            SELECT winner
            FROM races
            WHERE session_id=?
            ORDER BY id
            """,
            (session_id,)
        )

        return [row[0] for row in self.cursor.fetchall()]


    def delete_last_race(self, session_id):

        self.cursor.execute(
            """
            DELETE FROM races
            WHERE id = (

                SELECT id

                FROM races

                WHERE session_id=?

                ORDER BY id DESC

                LIMIT 1

            )
            """,
            (session_id,)
        )

        self.connection.commit()

    def save_strategy_statistic(
        self,
        strategy_name,
        rule_name,
        triggers,
        wins,
        losses
    ):

        self.cursor.execute("""
        INSERT INTO strategy_statistics(
            strategy_name,
            rule_name,
            triggers,
            wins,
            losses,
            last_updated
        )
        VALUES(
            ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        ON CONFLICT(strategy_name, rule_name)
        DO UPDATE SET

            triggers = excluded.triggers,
            wins = excluded.wins,
            losses = excluded.losses,
            last_updated = CURRENT_TIMESTAMP

        """, (

            strategy_name,
            rule_name,
            triggers,
            wins,
            losses

        ))

        self.connection.commit()

    def get_strategy_statistics(self):

        self.cursor.execute("""

            SELECT *

            FROM strategy_statistics

        """)

        return self.cursor.fetchall()
        