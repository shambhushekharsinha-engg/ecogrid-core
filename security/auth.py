"""
EcoGrid Security & Authentication Engine
Handles salted PBKDF2 password hashing, password policy enforcement,
user registration, login verification, and 100% fail-safe 1-click demo presets.
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

    def register_user(self, username: str, password: str, role: str = "Operator", force_update: bool = False) -> tuple[bool, str]:
        """Registers a new user or updates credentials if force_update is True."""
        clean_username = username.strip().lower()
        if not clean_username or len(clean_username) < 3:
            return False, "Username must be at least 3 characters long."

        is_valid, msg = self.validate_password_strength(password)
        if not is_valid and not force_update:
            return False, msg

        pwd_hash, salt = self._hash_password(password)

        try:
            conn = db_manager.get_connection()
            if db_manager.use_postgres:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT id FROM users WHERE LOWER(username) = %s;", (clean_username,))
                        existing = cur.fetchone()
                        if existing and not force_update:
                            return False, f"Username '{clean_username}' is already taken."
                        elif existing and force_update:
                            cur.execute("""
                                UPDATE users SET password_hash = %s, salt = %s, role = %s
                                WHERE LOWER(username) = %s;
                            """, (pwd_hash, salt, role, clean_username))
                        else:
                            cur.execute("""
                                INSERT INTO users (username, password_hash, salt, role)
                                VALUES (%s, %s, %s, %s);
                            """, (clean_username, pwd_hash, salt, role))
            else:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM users WHERE LOWER(username) = ?;", (clean_username,))
                    existing = cur.fetchone()
                    if existing and not force_update:
                        return False, f"Username '{clean_username}' is already taken."
                    elif existing and force_update:
                        cur.execute("""
                            UPDATE users SET password_hash = ?, salt = ?, role = ?
                            WHERE LOWER(username) = ?;
                        """, (pwd_hash, salt, role, clean_username))
                    else:
                        cur.execute("""
                            INSERT INTO users (username, password_hash, salt, role)
                            VALUES (?, ?, ?, ?);
                        """, (clean_username, pwd_hash, salt, role))
                conn.close()
            return True, f"User '{clean_username}' registered successfully!"
        except Exception as e:
            return False, f"Database error during registration: {str(e)}"

    def authenticate_user(self, username: str, password: str) -> tuple[bool, dict | str]:
        """Authenticates user credentials against stored salted hash with fail-safe demo fallback."""
        clean_username = username.strip().lower()

        # 1. Direct fail-safe check for Demo Presets
        if clean_username in self.DEMO_USERS:
            demo_meta = self.DEMO_USERS[clean_username]
            if password == demo_meta["password"]:
                # Ensure updated in DB in background
                try:
                    self.register_user(clean_username, demo_meta["password"], demo_meta["role"], force_update=True)
                except Exception:
                    pass
                return True, {
                    "username": clean_username,
                    "role": demo_meta["role"],
                    "token": f"ecogrid_sec_token_{secrets.token_hex(8)}"
                }

        # 2. Database authentication check for registered users
        try:
            conn = db_manager.get_connection()
            user_data = None
            if db_manager.use_postgres:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT username, password_hash, salt, role FROM users WHERE LOWER(username) = %s;", (clean_username,))
                        user_data = cur.fetchone()
            else:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT username, password_hash, salt, role FROM users WHERE LOWER(username) = ?;", (clean_username,))
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
                    "token": f"ecogrid_sec_token_{secrets.token_hex(8)}"
                }
            return False, "Invalid username or password."
        except Exception as e:
            return False, f"Authentication system error: {str(e)}"

    _demo_users_ensured = False

    def ensure_demo_users(self):
        """Auto-provisions standard demo accounts if not already present."""
        if AuthManager._demo_users_ensured:
            return
        for username, meta in self.DEMO_USERS.items():
            try:
                conn = db_manager.get_connection()
                user_exists = False
                if db_manager.use_postgres:
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT id FROM users WHERE LOWER(username) = %s;", (username.lower(),))
                            user_exists = bool(cur.fetchone())
                else:
                    with conn:
                        cur = conn.cursor()
                        cur.execute("SELECT id FROM users WHERE LOWER(username) = ?;", (username.lower(),))
                        user_exists = bool(cur.fetchone())
                    conn.close()

                if not user_exists:
                    self.register_user(username, meta["password"], meta["role"])
            except Exception:
                pass
        AuthManager._demo_users_ensured = True

auth_manager = AuthManager()
