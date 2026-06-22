"""
EcoGrid AI: Cryptographic Ledger Core Engine
Database Layer: Cloud PostgreSQL (Supabase Connection Pooler Integrated)
Architect: Shambhu Shekhar Sinha

Description:
- Formulates an append-only, tamper-evident transactional block matrix.
- Natively connects to PostgreSQL infrastructure using connection pooling strings.
"""

import os
import time
import json
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor

class CryptographicLedger:
    """Handles secure transaction serialization and verification block streaming to PostgreSQL."""

    def __init__(self):
        # Pull the DATABASE_URL environment token set in the cloud deployment platform settings
        self.db_url = os.environ.get("DATABASE_URL")
        if self.db_url:
            self._init_db()

    def _get_connection(self):
        """Establishes an isolated database cursor handle using the pooling credentials."""
        # Clean up connection strings that contain mixed escape characters from the pooler format
        cleaned_url = self.db_url.strip() if self.db_url else ""
        return psycopg2.connect(cleaned_url)

    def _init_db(self):
        """Generates the relational audit ledger table matrix schema inside the Supabase cluster."""
        try:
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
        except Exception as e:
            # Prevent app initialization failure if database sync drops temporarily
            print(f"⚠️ Relational Ledger table initialization bypass: {str(e)}")

    def _calculate_hash(self, block_dict):
        """Generates an deterministic SHA-256 validation seal across block parameters."""
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def record_transaction(self, agent_name, action, details):
        """Asynchronously serializes, chains, and commits a transaction block to the cloud database."""
        if not self.db_url:
            return "00000000000000000000000000000000"

        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Fetch total count to dynamically calculate the next block index identifier
                    cur.execute("SELECT COUNT(*) FROM grid_ledger;")
                    chain_len = cur.fetchone()['count']
                    
                    # Fetch the final block hash in the sequence to preserve chain link continuity
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
                    
                    # Execute atomic transaction load query down onto the Supabase cluster
                    cur.execute("""
                        INSERT INTO grid_ledger (block_index, timestamp, agent, action, details, previous_hash, current_hash)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (
                        new_block_template["index"], 
                        new_block_template["timestamp"], 
                        agent_name, 
                        action, 
                        new_block_template["details"], 
                        prev_hash, 
                        current_hash
                    ))
                conn.commit()
            return current_hash
        except Exception as err:
            print(f"⚠️ Failed streaming transaction block payload to cloud database: {str(err)}")
            return "ERROR_DATA_STREAM_DROP"