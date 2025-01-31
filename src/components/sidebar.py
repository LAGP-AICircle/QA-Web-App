import streamlit as st
import streamlit_antd_components as sac

def show_sidebar():
    """サイドバーを表示"""
    # デフォルトのサイドバーメニューを非表示にするCSS
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none; } /* デフォルトのページリストを非表示 */
        </style>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("QA Division Support")

        # メニューの実装
        selected = sac.menu(
            items=[
                sac.MenuItem('Home',
                            icon='house-fill',

                            description='ダッシュボード'),
                sac.MenuItem('Chatbot',
                            icon='chat-fill',
                            description='チャットボット'),
            ],
            format_func='title',
            open_all=True,
            indent=24
        )
        # ページ遷移の処理
        if selected:
            if selected == 'Chatbot':
                st.switch_page("pages/chatbot.py")
            elif selected == 'Home':
                st.switch_page("pages/home.py")

        # ユーザー情報とログアウトボタンの表示
        if st.session_state.get("logged_in_email"):
            st.markdown("---")
            st.markdown(f"ユーザー: {st.session_state['logged_in_email']}")
            # st.markdown(f"権限: {st.session_state['user']['role']}")

            # ログアウトボタン
            if st.button("ログアウト", use_container_width=True):
                st.session_state.authentication_status = False
                st.session_state.logged_in_email = None
                st.rerun()
