import streamlit as st
from auth import verify_login, save_user, change_password

# 許可されたドメインのリスト
ALLOWED_DOMAINS = ["lberc-g.jp", "alt-g.jp"]


def is_valid_email_domain(email: str) -> bool:
    """メールアドレスのドメインが許可されたものかチェック"""
    try:
        domain = email.split("@")[1]
        return domain in ALLOWED_DOMAINS
    except:
        return False


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
        # 表示モードの初期化
        if "display_mode" not in st.session_state:
            st.session_state.display_mode = "login"

        if st.session_state.display_mode == "login":
            # ログインフォーム
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

            # 新規登録とパスワード変更のボタンを横に並べる
            col1, col2 = st.columns(2)
            with col1:
                if st.button("新規登録", use_container_width=True):
                    st.session_state.display_mode = "signup"
                    st.rerun()
            with col2:
                if st.button("パスワード変更", use_container_width=True):
                    st.session_state.display_mode = "change_password"
                    st.rerun()

        elif st.session_state.display_mode == "signup":
            # 新規登録フォーム
            with st.form("signup_form"):
                st.subheader("新規登録")
                new_email = st.text_input("メールアドレス")
                new_password = st.text_input("パスワード", type="password")
                confirm_password = st.text_input("パスワード（確認）", type="password")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    signup_submitted = st.form_submit_button("登録", use_container_width=True)

                if signup_submitted:
                    if not new_email or not new_password or not confirm_password:
                        st.error("すべての項目を入力してください")
                    elif new_password != confirm_password:
                        st.error("パスワードが一致しません")
                    elif not is_valid_email_domain(new_email):
                        st.error(
                            "このメールアドレスのドメインは許可されていません。@lberc-g.jp または @alt-g.jp のメールアドレスを使用してください。"
                        )
                    else:
                        save_user(new_email, new_password)
                        st.success("登録が完了しました")
                        st.session_state.display_mode = "login"
                        st.rerun()

            # ログイン画面に戻るボタン
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("ログイン画面に戻る", use_container_width=True):
                    st.session_state.display_mode = "login"
                    st.rerun()

        elif st.session_state.display_mode == "change_password":
            # パスワード変更フォーム
            with st.form("change_password_form"):
                st.subheader("パスワード変更")
                email = st.text_input("メールアドレス")
                new_password = st.text_input("新しいパスワード", type="password")
                confirm_password = st.text_input("新しいパスワード（確認）", type="password")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    change_submitted = st.form_submit_button("パスワード変更", use_container_width=True)

                if change_submitted:
                    if not email or not new_password or not confirm_password:
                        st.error("すべての項目を入力してください")
                    elif new_password != confirm_password:
                        st.error("パスワードが一致しません")
                    elif not is_valid_email_domain(email):
                        st.error(
                            "このメールアドレスのドメインは許可されていません。@lberc-g.jp または @alt-g.jp のメールアドレスを使用してください。"
                        )
                    elif change_password(email, new_password):
                        st.success("パスワードを変更しました")
                        st.session_state.display_mode = "login"
                        st.rerun()
                    else:
                        st.error("メールアドレスが見つかりません")

            # ログイン画面に戻るボタン
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("ログイン画面に戻る", use_container_width=True):
                    st.session_state.display_mode = "login"
                    st.rerun()
