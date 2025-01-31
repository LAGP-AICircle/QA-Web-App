import hashlib
from pathlib import Path
import json

def hash_password(password: str) -> str:
    """パスワードをハッシュ化"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(email: str, password: str) -> bool:
    """ログイン認証を行う"""
    hashed_password = hash_password(password)
    credentials_path = Path("data/credentials.json")

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
    credentials_path = Path("data/credentials.json")

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