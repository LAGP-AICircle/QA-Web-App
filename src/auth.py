import hashlib
import sqlite3
from pathlib import Path
import os
from typing import List, Dict
from datetime import datetime


def hash_password(password: str) -> str:
    """パスワードをハッシュ化"""
    return hashlib.sha256(password.encode()).hexdigest()


def get_db_path() -> Path:
    """SQLiteのDBファイルパスを取得"""
    # スクリプトのディレクトリを基準にパスを構築
    current_dir = Path(__file__).parent
    db_dir = current_dir / "data"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "users.db"


def init_db():
    """データベースの初期化"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # usersテーブルの作成
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def verify_login(email: str, password: str) -> bool:
    """ログイン認証を行う"""
    init_db()  # DB初期化
    hashed_password = hash_password(password)

    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        c.execute("SELECT 1 FROM users WHERE email = ? AND password_hash = ?", (email, hashed_password))
        result = c.fetchone() is not None
        return result
    except Exception as e:
        print(f"認証エラー: {str(e)}")
        return False
    finally:
        conn.close()


def save_user(email: str, password: str, is_admin: bool = False):
    """新規ユーザーを保存する"""
    init_db()  # DB初期化
    hashed_password = hash_password(password)

    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (email, password_hash, is_admin) VALUES (?, ?, ?)", (email, hashed_password, is_admin)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("このメールアドレスは既に登録されています")
    except Exception as e:
        raise Exception(f"ユーザー登録エラー: {str(e)}")
    finally:
        conn.close()


def change_password(email: str, new_password: str) -> bool:
    """パスワードを変更する

    Args:
        email (str): メールアドレス
        new_password (str): 新しいパスワード

    Returns:
        bool: 変更成功ならTrue、メールアドレスが存在しない場合はFalse
    """
    init_db()  # DB初期化
    hashed_password = hash_password(new_password)

    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        # メールアドレスが存在するか確認
        c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        if c.fetchone() is None:
            return False

        # パスワードを更新
        c.execute(
            """
            UPDATE users 
            SET password_hash = ?, 
                updated_at = CURRENT_TIMESTAMP 
            WHERE email = ?
        """,
            (hashed_password, email),
        )
        conn.commit()
        return True

    except Exception as e:
        print(f"パスワード変更エラー: {str(e)}")
        return False
    finally:
        conn.close()


# 既存のユーザーデータを移行
def migrate_existing_users():
    """既存のcredentials.jsonからSQLiteへデータを移行"""
    credentials_path = Path(__file__).parent / "data" / "credentials.json"
    if not credentials_path.exists():
        return

    import json

    with open(credentials_path, "r") as f:
        credentials = json.load(f)

    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        for email, password_hash in credentials.items():
            try:
                c.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, password_hash))
            except sqlite3.IntegrityError:
                # 既に存在する場合はスキップ
                continue
        conn.commit()
    finally:
        conn.close()


def is_admin(email: str) -> bool:
    """ユーザーが管理者かどうかを確認する"""
    init_db()
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        c.execute("SELECT is_admin FROM users WHERE email = ?", (email,))
        result = c.fetchone()
        return bool(result[0]) if result else False
    except Exception as e:
        print(f"管理者確認エラー: {str(e)}")
        return False
    finally:
        conn.close()


def get_all_users() -> List[Dict]:
    """登録されているすべてのユーザー情報を取得"""
    init_db()  # DB初期化
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        c.execute(
            """
            SELECT email, is_admin, created_at, updated_at 
            FROM users 
            ORDER BY created_at DESC
        """
        )

        users = []
        for row in c.fetchall():
            users.append({"email": row[0], "is_admin": bool(row[1]), "created_at": row[2], "updated_at": row[3]})
        return users

    except Exception as e:
        print(f"ユーザー一覧取得エラー: {str(e)}")
        return []
    finally:
        conn.close()


def delete_user(email: str) -> bool:
    """ユーザーを削除する

    Args:
        email (str): 削除するユーザーのメールアドレス

    Returns:
        bool: 削除成功ならTrue、ユーザーが存在しない場合はFalse
    """
    init_db()
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    try:
        # メールアドレスが存在するか確認
        c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        if c.fetchone() is None:
            return False

        # ユーザーを削除
        c.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
        return True

    except Exception as e:
        print(f"ユーザー削除エラー: {str(e)}")
        return False
    finally:
        conn.close()
