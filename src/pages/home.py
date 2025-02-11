import streamlit as st


def show_home_page():
    """ホーム画面を表示"""
    # 現在のページがホームでない場合は即座に終了
    if st.session_state.page != "home":
        return

    # ログインチェック
    if not st.session_state.get("password_correct", False):
        st.error("ログインが必要です")
        st.stop()

    # メインコンテンツ
    st.title("QA Support System")
    st.write("左サイドバーのメニューから機能を選択してください。")

    # お知らせメッセージ
    st.info("お知らせ: システムをご利用いただきありがとうございます。")


if __name__ == "__main__":
    show_home_page()
