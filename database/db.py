"""
Database Abstraction Layer for EcoGrid & Aegis Traffic Infrastructure
Supports SQLite (Local zero-dependency fallback) and PostgreSQL (Production Cloud setup).
Includes automatic failover to SQLite if PostgreSQL connection fails.
"""

import os
import sqlite3

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(__file__), "ecogrid_aegis.db")

class DatabaseManager:
    """Unified Database Interface supporting SQLite and PostgreSQL with auto-failover."""

    def __init__(self, db_url=None):
        self.db_url = db_url or os.environ.get("DATABASE_URL")
        self.use_postgres = bool(self.db_url and HAS_PSYCOPG2)
        self.sqlite_path = DEFAULT_SQLITE_PATH
        self.init_db()

    def get_connection(self):
        """Returns database connection, with automatic failover from Postgres to SQLite."""
        if self.use_postgres:
            try:
                cleaned_url = self.db_url.strip()
                return psycopg2.connect(cleaned_url, connect_timeout=3)
            except Exception as e:
                print(f"⚠️ Postgres connection failed ({e}), automatically falling back to embedded SQLite.")
                self.use_postgres = False

        os.makedirs(os.path.dirname(self.sqlite_path), exist_ok=True)
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes system tables for Users and Cryptographic Grid Ledger."""
        if self.use_postgres:
            try:
                conn = self.get_connection()
                if self.use_postgres:
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                CREATE TABLE IF NOT EXISTS users (
                                    id SERIAL PRIMARY KEY,
                                    username VARCHAR(50) UNIQUE NOT NULL,
                                    password_hash VARCHAR(128) NOT NULL,
                                    salt VARCHAR(64) NOT NULL,
                                    role VARCHAR(30) NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                                CREATE TABLE IF NOT EXISTS grid_ledger (
                                    id SERIAL PRIMARY KEY,
                                    block_index INT NOT NULL,
                                    timestamp TEXT NOT NULL,
                                    agent TEXT NOT NULL,
                                    action TEXT NOT NULL,
                                    details TEXT NOT NULL,
                                    previous_hash TEXT NOT NULL,
                                    current_hash TEXT NOT NULL
                                );
                            """)
                    conn.close()
                    return
            except Exception as e:
                print(f"⚠️ Postgres DB init warning ({e}), falling back to SQLite.")
                self.use_postgres = False

        # SQLite Database Initialization
        try:
            os.makedirs(os.path.dirname(self.sqlite_path), exist_ok=True)
            with sqlite3.connect(self.sqlite_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        role TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS grid_ledger (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        block_index INTEGER NOT NULL,
                        timestamp TEXT NOT NULL,
                        agent TEXT NOT NULL,
                        action TEXT NOT NULL,
                        details TEXT NOT NULL,
                        previous_hash TEXT NOT NULL,
                        current_hash TEXT NOT NULL
                    );
                """)
                conn.commit()
        except Exception as e:
            print(f"⚠️ SQLite DB init error: {e}")

db_manager = DatabaseManager()
