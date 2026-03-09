import sqlite3
import json
from pathlib import Path
from schemas.paper import Paper


DB_PATH = Path("memory/papers.db")


class PaperStore:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

    def create_table(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS papers(
            id TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            year INTEGER,
            abstract TEXT,
            url TEXT,
            source TEXT
        )
        """)

    def insert(self, paper: Paper):

        self.conn.execute("""
        INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?,?)
        """, (
            paper.id,
            paper.title,
            json.dumps(paper.authors),
            paper.year,
            paper.abstract,
            paper.url,
            paper.source
        ))

        self.conn.commit()

    def get_by_id(self, pid: str):

        cur = self.conn.execute(
            "SELECT * FROM papers WHERE id=?", (pid,)
        )

        return cur.fetchone()