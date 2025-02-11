import streamlit as st
import streamlit_antd_components as sac
from pages.chatbot import load_system_prompts


def show_sidebar():
    """サイドバーを表示"""
    with st.sidebar:
        st.title("QA Division Support")

        # メニューの実装
        selected = sac.menu(
            items=[
                sac.MenuItem("Home", icon="house-fill", description="ダッシュボード"),
                sac.MenuItem("Chatbot", icon="chat-fill", description="チャットボット"),
            ],
            format_func="title",
            open_all=True,
            indent=24,
            key="main_menu",
        )

        # ページ遷移の処理
        if selected:
            page_mapping = {"Home": "home", "Chatbot": "chatbot"}
            if selected in page_mapping:
                st.session_state.page = page_mapping[selected]

        # チャットボット設定（チャットボットページの場合のみ表示）
        if st.session_state.page == "chatbot":
            # SYSTEM_PROMPTSの初期化
            if "SYSTEM_PROMPTS" not in st.session_state:
                st.session_state.SYSTEM_PROMPTS = load_system_prompts()

            if st.session_state.SYSTEM_PROMPTS:
                st.markdown("---")
                st.subheader("チャットボット設定")
                st.selectbox(
                    "カテゴリを選択してください",
                    options=list(st.session_state.SYSTEM_PROMPTS.keys()),
                    key="chatbot_category",
                )
                if st.button("会話履歴をクリア", key="clear_chat_history"):
                    st.session_state.messages = []
                    st.rerun()

        # ユーザー情報とログアウトボタンの表示
        if st.session_state.get("logged_in_email"):
            st.markdown("---")
            with st.container():
                if st.button("ログアウト", key="logout_button", use_container_width=True):
                    st.session_state.password_correct = False
                    st.session_state.logged_in_email = None
                    st.rerun()
