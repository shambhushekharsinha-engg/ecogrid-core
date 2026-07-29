"""
EcoGrid & Aegis Traffic: Cryptographic Ledger Engine
Handles tamper-evident transaction serialization, SHA-256 block chaining,
and verification across Postgres / SQLite / JSON persistence layers.
"""

import os
import time
import json
import hashlib
from database.db import db_manager

class CryptographicLedger:
    """Append-only tamper-evident transactional block chain manager."""

    def __init__(self, json_file_path="reports/ledger.json"):
        self.json_file_path = json_file_path
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        if not os.path.exists(self.json_file_path):
            with open(self.json_file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _calculate_hash(self, block_dict: dict) -> str:
        """Generates a deterministic SHA-256 validation seal for a block."""
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def record_transaction(self, agent_name: str, action: str, details: dict) -> str:
        """Serializes, chains, and commits a transaction block to database and JSON audit file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        details_str = json.dumps(details) if isinstance(details, dict) else str(details)

        # 1. Load local JSON ledger for fallback and fast frontend rendering
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                local_blocks = json.load(f)
        except Exception:
            local_blocks = []

        prev_hash = local_blocks[-1]["current_hash"] if local_blocks else "00000000000000000000000000000000"
        block_index = len(local_blocks) + 1

        new_block = {
            "index": block_index,
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details,
            "previous_hash": prev_hash
        }
        current_hash = self._calculate_hash(new_block)
        new_block["current_hash"] = current_hash

        local_blocks.append(new_block)

        try:
            with open(self.json_file_path, "w", encoding="utf-8") as f:
                json.dump(local_blocks, f, indent=2)
        except Exception as e:
            print(f"⚠️ Local JSON ledger update error: {e}")

        # 2. Persist to relational DB
        try:
            conn = db_manager.get_connection()
            if db_manager.use_postgres:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO grid_ledger (block_index, timestamp, agent, action, details, previous_hash, current_hash)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """, (block_index, timestamp, agent_name, action, details_str, prev_hash, current_hash))
            else:
                with conn:
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO grid_ledger (block_index, timestamp, agent, action, details, previous_hash, current_hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, (block_index, timestamp, agent_name, action, details_str, prev_hash, current_hash))
                conn.close()
        except Exception as e:
            print(f"⚠️ Relational ledger record note: {e}")

        return current_hash

    def verify_chain(self) -> tuple[bool, str]:
        """Verifies the SHA-256 hash link continuity of the ledger blocks."""
        try:
            with open("reports/ledger.json", "r", encoding="utf-8") as f:
                blocks = json.load(f)
            
            if not blocks:
                return True, "Ledger is empty. Chain integrity nominal."

            for i in range(len(blocks)):
                block = blocks[i]
                if i > 0 and block["previous_hash"] != blocks[i - 1]["current_hash"]:
                    return False, f"Broken chain link detected at block index {block['index']}!"

                calc_payload = {
                    "index": block["index"],
                    "timestamp": block["timestamp"],
                    "agent": block["agent"],
                    "action": block["action"],
                    "details": block["details"],
                    "previous_hash": block["previous_hash"]
                }
                calc_hash = self._calculate_hash(calc_payload)
                if calc_hash != block["current_hash"]:
                    return False, f"Tampered block hash at index {block['index']}!"

            return True, f"All {len(blocks)} blocks cryptographically verified and valid."
        except Exception as e:
            return False, f"Verification failed: {str(e)}"