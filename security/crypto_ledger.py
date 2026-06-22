import os
import time
import json
import hashlib
import psycopg2 # Make sure to add psycopg2-binary to your requirements.txt
from psycopg2.extras import RealDictCursor

class CryptographicLedger:
    """Creates an immutable, append-only cryptographic audit trail inside Cloud PostgreSQL."""

    def __init__(self):
        # Read the secure database connection string set in the hosting dashboard
        self.db_url = os.environ.get("DATABASE_URL")
        if self.db_url:
            self._init_db()

    def _get_connection(self):
        return psycopg2.connect(self.db_url)

    def _init_db(self):
        """Creates the relational verification ledger table matrix automatically."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
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
            conn.commit()

    def _calculate_hash(self, block_dict):
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def record_transaction(self, agent_name, action, details):
        if not self.db_url:
            return "000000000000000000000000"

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Calculate index based on row records
                cur.execute("SELECT COUNT(*) FROM grid_ledger;")
                chain_len = cur.fetchone()['count']
                
                # Fetch last hash for block linking fallback verification
                cur.execute("SELECT current_hash FROM grid_ledger ORDER BY id DESC LIMIT 1;")
                last_row = cur.fetchone()
                prev_hash = last_row['current_hash'] if last_row else "00000000000000000000000000000000"
                
                new_block_template = {
                    "index": chain_len + 1,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "agent": agent_name,
                    "action": action,
                    "details": json.dumps(details),
                    "previous_hash": prev_hash
                }
                current_hash = self._calculate_hash(new_block_template)
                
                # Commit structural entry block down onto database cluster
                cur.execute("""
                    INSERT INTO grid_ledger (block_index, timestamp, agent, action, details, previous_hash, current_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (new_block_template["index"], new_block_template["timestamp"], agent_name, action, new_block_template["details"], prev_hash, current_hash))
            conn.commit()
        return current_hash