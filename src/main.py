import streamlit as st
from ui.login_ui import show_login_page
from ui.signup_ui import show_signup_page
from components.sidebar import show_sidebar
from pages.home import show_home_page
from pages.chatbot import show_chatbot_page
from pages.qa_drill import show_qa_drill_page
from pages.admin import show_admin_page


def init_session_state():
    """セッション状態の初期化"""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "is_signup_visible" not in st.session_state:
        st.session_state.is_signup_visible = False


def init_page(is_logged_in: bool):
    """ページの初期化"""
    st.set_page_config(
        page_title="QA事業部 Home",
        page_icon=":speech_balloon:",
        layout="wide",
        initial_sidebar_state="expanded" if is_logged_in else "collapsed",
        menu_items={"Get Help": None, "Report a bug": None, "About": None},
    )

    # デフォルトのページナビゲーションを非表示
    hide_pages = """
        <style>
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            [data-testid="stSidebarNav"] {display: none !important;}
            button[kind="header"] {display: none !important;}
        </style>
    """
    st.markdown(hide_pages, unsafe_allow_html=True)


def show_current_page():
    """現在のページを表示"""
    # コンテナを作成してページをクリア
    main_container = st.container()
    main_container.empty()

    with main_container:
        # ページに応じたコンテンツを表示
        if st.session_state.page == "chatbot":
            show_chatbot_page()
        elif st.session_state.page == "qa_drill":
            show_qa_drill_page()
        elif st.session_state.page == "admin":
            show_admin_page()
        elif st.session_state.page == "home":
            show_home_page()


def main():
    """メイン処理"""
    # セッション状態の初期化
    init_session_state()

    # ページ設定の初期化
    init_page(st.session_state.password_correct)

    # ログインしていない場合はログイン/サインアップ画面を表示
    if not st.session_state.password_correct:
        if st.session_state.is_signup_visible:
            show_signup_page()
        else:
            show_login_page()
    else:
        # ログイン時はサイドバーとメインコンテンツを表示
        show_sidebar()
        show_current_page()


if __name__ == "__main__":
    main()
