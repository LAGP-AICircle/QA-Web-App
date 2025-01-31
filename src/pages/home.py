import streamlit as st
from components.sidebar import show_sidebar

def show_home_page():
    """ホーム画面を表示"""

    # ログインチェック
    if not st.session_state.get("password_correct", False):
        st.error("ログインが必要です")
        st.stop()

    # サイドバーを表示
    show_sidebar()
    
    # メインコンテンツ
    st.title("QA サポートシステム")
    st.write("左サイドバーのメニューから機能を選択してください。")

    # お知らせメッセージ
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("お知らせ: システムをご利用いただきありがとうございます。")

if __name__ == "__main__":
    show_home_page()