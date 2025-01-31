import streamlit as st
import re
from auth import save_user

def is_valid_email(email: str) -> bool:
    """メールアドレスの形式が正しいかチェックする"""
    allowed_domains = ["@alt-g.jp", "@lberc-g.jp"]
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None and any(domain in email for domain in allowed_domains)

def show_signup_page():
    """新規登録画面を表示する"""
    col1, col2, col3 = st.columns([3.5, 1, 3.5])
    with col2:
        st.title("新規登録")

    # 登録フォーム
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("signup_form"):
            email = st.text_input("メールアドレス")
            password = st.text_input("パスワード", type="password")
            password_confirm = st.text_input("パスワード（確認）", type="password")

            # 登録ボタン中央に配置
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("登録", use_container_width=True)

        if submit_button:
            if not email or not password:
                st.error("メールドレスとパスワードを入力してください")
            elif not is_valid_email(email):
                st.error("有効なメールアドレスを入力してください")
            elif password != password_confirm:
                st.error("パスワードが一致しません")
            else:
                try:
                    # 新規ユーザーを保存
                    save_user(email, password)
                    st.success("ユーザー登録が完了しました")

                    # 登録完了後、自動的にログイン画面に戻る
                    st.session_state["is_signup_visible"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"登録に失敗しました: {str(e)}")

        # 区切り線を追加
        st.markdown("---")
    
        # ログイン画面に戻るボタン
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("戻る", use_container_width=True):
                st.session_state["is_signup_visible"] = False
                st.rerun()