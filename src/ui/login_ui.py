import streamlit as st
from auth import verify_login


def show_login_page():
    """ログイン画面を表示"""
    # カスタムCSSでタイトルを中央配置
    st.markdown(
        """
        <style>
        .title-container {
            margin: 0;
            padding: 3rem 0;
            text-align: center;
        }
        .title-container h1 {
            color: #0066cc;
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }
        </style>
        <div class="title-container">
            <h1>QA事業部 SupportSystem</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # スペースを追加してフォームとの間隔を確保
    st.markdown("<br><br>", unsafe_allow_html=True)

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
