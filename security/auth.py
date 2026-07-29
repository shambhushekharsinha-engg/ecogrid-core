"""
Aegis & EcoGrid Security & Authentication Engine
Handles salted PBKDF2 password hashing, password policy enforcement,
user registration, login verification, and 1-click demo presets.
"""

import hashlib
import secrets
import re
import sqlite3
from database.db import db_manager

class AuthManager:
    """Manages user authentication, security policies, and session credentials."""

    DEMO_USERS = {
        "admin": {"password": "Admin@123", "role": "System Administrator"},
        "traffic_op": {"password": "Traffic@123", "role": "Traffic Operations Chief"},
        "grid_eng": {"password": "Grid@123", "role": "Microgrid Chief Engineer"},
        "guest": {"password": "Guest@123", "role": "Guest Auditor"}
    }

    def __init__(self):
        self.ensure_demo_users()

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Enforces strong password policy (min 8 chars, uppercase, lowercase, digit/special char)."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[\d\W]", password):
            return False, "Password must contain at least one digit or special character."
        return True, "Password meets security requirements."

    @staticmethod
    def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
        """Hashes password using PBKDF2 HMAC SHA-256 with 100,000 iterations and a unique salt."""
        if not salt:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return pwd_hash, salt

    def register_user(self, username: str, password: str, role: str = "Operator") -> tuple[bool, str]:
        """Registers a new user after validating username and password strength."""
        username = username.strip()
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long."

        is_valid, msg = self.validate_password_strength(password)
        if not is_valid:
            return False, msg

        pwd_hash, salt = self._hash_password(password)

        try:
            conn = db_manager.get_connection()
            if db_manager.use_postgres:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
                        if cur.fetchone():
                            return False, f"Username '{username}' is already taken."
                        cur.execute("""
                            INSERT INTO users (username, password_hash, salt, role)
                            VALUES (%s, %s, %s, %s);
                        """, (username, pwd_hash, salt, role))
            else:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM users WHERE username = ?;", (username,))
                    if cur.fetchone():
                        return False, f"Username '{username}' is already taken."
                    cur.execute("""
                        INSERT INTO users (username, password_hash, salt, role)
                        VALUES (?, ?, ?, ?);
                    """, (username, pwd_hash, salt, role))
                conn.close()
            return True, f"User '{username}' registered successfully!"
        except Exception as e:
            return False, f"Database error during registration: {str(e)}"

    def authenticate_user(self, username: str, password: str) -> tuple[bool, dict | str]:
        """Authenticates user credentials against stored salted hash."""
        username = username.strip()
        try:
            conn = db_manager.get_connection()
            user_data = None
            if db_manager.use_postgres:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT username, password_hash, salt, role FROM users WHERE username = %s;", (username,))
                        user_data = cur.fetchone()
            else:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT username, password_hash, salt, role FROM users WHERE username = ?;", (username,))
                    user_data = cur.fetchone()
                conn.close()

            if not user_data:
                return False, "Invalid username or password."

            if isinstance(user_data, sqlite3.Row) or isinstance(user_data, dict):
                stored_username = user_data["username"]
                stored_hash = user_data["password_hash"]
                stored_salt = user_data["salt"]
                stored_role = user_data["role"]
            else:
                stored_username, stored_hash, stored_salt, stored_role = user_data

            computed_hash, _ = self._hash_password(password, stored_salt)
            if secrets.compare_digest(stored_hash, computed_hash):
                return True, {
                    "username": stored_username,
                    "role": stored_role,
                    "token": f"aegis_sec_token_{secrets.token_hex(8)}"
                }
            return False, "Invalid username or password."
        except Exception as e:
            return False, f"Authentication system error: {str(e)}"

    def ensure_demo_users(self):
        """Auto-provisions standard demo accounts for 1-click quick login access."""
        for username, meta in self.DEMO_USERS.items():
            try:
                self.register_user(username, meta["password"], meta["role"])
            except Exception:
                pass

auth_manager = AuthManager()
