import hashlib
from pathlib import Path
import json
import os


def hash_password(password: str) -> str:
    """パスワードをハッシュ化"""
    return hashlib.sha256(password.encode()).hexdigest()


def get_credentials_path() -> Path:
    """credentials.jsonのパスを取得"""
    # スクリプトのディレクトリを基準にパスを構築
    current_dir = Path(__file__).parent
    return current_dir / "data" / "credentials.json"


def verify_login(email: str, password: str) -> bool:
    """ログイン認証を行う"""
    hashed_password = hash_password(password)
    credentials_path = get_credentials_path()

    # credentials.jsonが存在しない場合はFalseを返す
    if not credentials_path.exists():
        return False

    try:
        with open(credentials_path, "r") as f:
            credentials = json.load(f)
            # credentials全体をチェック
            return credentials.get(email) == hashed_password

    except:
        return False


def save_user(email: str, password: str):
    """新規ユーザーをcredentials.jsonに保存する"""
    hashed_password = hash_password(password)
    credentials_path = get_credentials_path()

    # データディレクトリがない場合は作成
    credentials_path.parent.mkdir(parents=True, exist_ok=True)

    # 既存のユーザー情報を読み込む
    if credentials_path.exists():
        with open(credentials_path) as f:
            credentials = json.load(f)
    else:
        credentials = {}

    # ユーザー情報を追加
    credentials[email] = hashed_password

    # 設定ファイルに保存
    with open(credentials_path, "w") as f:
        json.dump(credentials, f)


def change_password(email: str, new_password: str) -> bool:
    """パスワードを変更する

    Args:
        email (str): メールアドレス
        new_password (str): 新しいパスワード

    Returns:
        bool: 変更成功ならTrue、メールアドレスが存在しない場合はFalse
    """
    credentials_path = get_credentials_path()

    # ファイルが存在しない場合はFalse
    if not credentials_path.exists():
        return False

    try:
        # 既存のユーザー情報を読み込む
        with open(credentials_path, "r") as f:
            credentials = json.load(f)

        # メールアドレスが存在しない場合はFalse
        if email not in credentials:
            return False

        # パスワードを更新
        credentials[email] = hash_password(new_password)

        # 保存
        with open(credentials_path, "w") as f:
            json.dump(credentials, f)

        return True

    except:
        return False
