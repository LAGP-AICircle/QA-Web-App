import sys
import os

# srcディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import save_user


def create_admin(email: str, password: str):
    """管理者ユーザーを作成"""
    try:
        save_user(email, password, is_admin=True)
        print(f"管理者ユーザー {email} を作成しました")
    except Exception as e:
        print(f"エラー: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python create_admin.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    create_admin(email, password)
