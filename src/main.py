import streamlit as st
from ui.login_ui import show_login_page
from ui.signup_ui import show_signup_page
from components.sidebar import show_sidebar  

def init_page(is_logged_in: bool):
    """ページの初期化"""
    st.set_page_config(
        page_title="QA事業部 Home",
        page_icon=":speech_balloon:",
        layout="wide",
        initial_sidebar_state="expanded" if is_logged_in else "collapsed"
    )

def main():
    """メイン処理"""
    # ログイン状態を取得
    is_logged_in = st.session_state.get("password_correct", False)
    init_page(is_logged_in)

    # ログインしていない場合はログイン/サインアップ画面を表示
    if not st.session_state.get("password_correct", False):
        if st.session_state.get("is_signup_visible", False):
            show_signup_page()
        else:
            show_login_page()
        # ログインしていない時のみサイドバーを非表示に
        st.markdown("""
            <style>
                [data-testid="collapsedControl"] { display: none; }
                section[data-testid="stSidebar"] { display: none; }
            </style>
            """, unsafe_allow_html=True)
    else:
        show_sidebar()  # ログイン時はsidebar.pyのサイドバーを表示
        # ログイン後は自動的にHomeページにリダイレクト
        st.switch_page("pages/home.py")

if __name__ == "__main__":
    main()