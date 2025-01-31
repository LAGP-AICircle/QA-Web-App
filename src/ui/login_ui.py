import streamlit as st
from auth import verify_login

def show_login_page():
    """ログイン画面を表示"""
    # タイトル表示
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.title("QA事業部 サポートシステム")

    # フォームを中央に配置するためのカラムレイアウト
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("メールアドレス")
            password = st.text_input("パスワード", type="password")

            # ログインボタンを中央に配置
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("ログイン", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("メールアドレスとパスワードを入力してください")
                elif verify_login(email, password):
                    st.session_state.password_correct = True
                    st.session_state.logged_in_email = email
                    st.rerun()
                else:
                    st.error("メールアドレスまたはパスワードが正しくありません")
        
        # 区切り線を追加
        st.markdown("---")
        
        # 新規登録ボタンをログインフォームの下に配置
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("新規登録", use_container_width=True):
                st.session_state["is_signup_visible"] = True
                st.rerun()