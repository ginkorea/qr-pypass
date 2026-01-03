from __future__ import annotations

import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any

from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash


def data_dir() -> Path:
    base = Path(os.environ.get("QRPYPASS_DATA_DIR", Path.home() / ".qrpypass"))
    base.mkdir(parents=True, exist_ok=True)
    return base


def db_path() -> Path:
    return data_dir() / "app.db"


def master_fernet() -> Fernet:
    key = os.environ.get("QRPYPASS_MASTER_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing QRPYPASS_MASTER_KEY (required in multi-user mode)")
    # QRPYPASS_MASTER_KEY must be a Fernet key (urlsafe base64 32 bytes).
    return Fernet(key.encode("utf-8"))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path()))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            pw_hash TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS totp_accounts (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            issuer TEXT,
            secret_enc BLOB NOT NULL,
            algorithm TEXT NOT NULL,
            digits INTEGER NOT NULL,
            period INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            UNIQUE(user_id, id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)


@dataclass
class User:
    id: int
    email: str

    # Flask-Login interface
    @property
    def is_authenticated(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_active(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_anonymous(self) -> bool:  # pragma: no cover
        return False

    def get_id(self) -> str:  # pragma: no cover
        return str(self.id)


def create_user(email: str, password: str) -> User:
    email = (email or "").strip().lower()
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if not password or len(password) < 10:
        raise ValueError("Password must be at least 10 characters")

    pw_hash = generate_password_hash(password)
    now = int(time.time())

    with connect() as c:
        try:
            cur = c.execute(
                "INSERT INTO users (email, pw_hash, created_at) VALUES (?, ?, ?)",
                (email, pw_hash, now),
            )
        except sqlite3.IntegrityError:
            raise ValueError("Email already registered")
        uid = int(cur.lastrowid)
    return User(id=uid, email=email)


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with connect() as c:
        r = c.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
        return r


def get_user_by_id(user_id: int) -> Optional[User]:
    with connect() as c:
        r = c.execute("SELECT id, email FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if not r:
            return None
        return User(id=int(r["id"]), email=str(r["email"]))


def authenticate(email: str, password: str) -> Optional[User]:
    r = get_user_by_email(email)
    if not r:
        return None
    if not check_password_hash(r["pw_hash"], password):
        return None
    return User(id=int(r["id"]), email=str(r["email"]))


def upsert_totp_account(
    *,
    user_id: int,
    acc_id: str,
    name: str,
    issuer: Optional[str],
    secret_b32: str,
    algorithm: str,
    digits: int,
    period: int,
) -> None:
    f = master_fernet()
    secret_enc = f.encrypt(secret_b32.encode("utf-8"))
    now = int(time.time())

    with connect() as c:
        c.execute(
            """
            INSERT INTO totp_accounts
              (id, user_id, name, issuer, secret_enc, algorithm, digits, period, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              user_id=excluded.user_id,
              name=excluded.name,
              issuer=excluded.issuer,
              secret_enc=excluded.secret_enc,
              algorithm=excluded.algorithm,
              digits=excluded.digits,
              period=excluded.period
            """,
            (acc_id, int(user_id), name, issuer, secret_enc, algorithm, int(digits), int(period), now),
        )


def list_totp_accounts(user_id: int) -> List[Dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT id, name, issuer, algorithm, digits, period, created_at FROM totp_accounts WHERE user_id = ? ORDER BY created_at DESC",
            (int(user_id),),
        ).fetchall()

    out = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "name": r["name"],
                "issuer": r["issuer"],
                "algorithm": r["algorithm"],
                "digits": int(r["digits"]),
                "period": int(r["period"]),
                "created_at": int(r["created_at"]),
            }
        )
    return out


def get_totp_account(user_id: int, acc_id: str) -> Optional[Dict[str, Any]]:
    with connect() as c:
        r = c.execute(
            "SELECT * FROM totp_accounts WHERE user_id = ? AND id = ?",
            (int(user_id), acc_id),
        ).fetchone()
        if not r:
            return None

    f = master_fernet()
    secret_b32 = f.decrypt(r["secret_enc"]).decode("utf-8")

    return {
        "id": r["id"],
        "name": r["name"],
        "issuer": r["issuer"],
        "secret_b32": secret_b32,
        "algorithm": r["algorithm"],
        "digits": int(r["digits"]),
        "period": int(r["period"]),
    }
