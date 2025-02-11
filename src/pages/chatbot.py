import streamlit as st
import os
from langsmith import wrappers, traceable
from auth import verify_login
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.openai_utils import get_openai_client


def load_system_prompts():
    """システムプロンプトの読み込み"""
    prompts = {}
    try:
        # 機能分類プロンプトの読み込み
        function_classification_path = os.path.join("src", "prompts", "function_classification.md")
        with open(function_classification_path, "r", encoding="utf-8") as f:
            prompts["機能分類"] = {"content": f.read(), "type": "markdown"}

        # テスト分類プロンプトの読み込み
        test_classification_path = os.path.join("src", "prompts", "test_classification.md")
        with open(test_classification_path, "r", encoding="utf-8") as f:
            prompts["テスト分類"] = {"content": f.read(), "type": "markdown"}

        # 評価シート作成プロンプトの読み込み
        evaluation_sheet_path = os.path.join("src", "prompts", "evaluation_sheet.md")
        with open(evaluation_sheet_path, "r", encoding="utf-8") as f:
            prompts["評価シート作成"] = {"content": f.read(), "type": "markdown"}

        return prompts
    except FileNotFoundError:
        st.error("システムプロンプトファイルが見つかりません。")
        st.info("管理者に連絡してください。")
        return {}
    except Exception as e:
        st.error(f"システムプロンプトの読み込み中にエラーが発生しました: {str(e)}")
        st.info("管理者に連絡してください。")
        return {}


def get_chat_response(system_prompt: str, user_input: str, message_placeholder, chat_history: list) -> str:
    """ストリーミング対応のチャット応答を取得"""
    try:
        # OpenAIクライアントの確認
        client = get_openai_client()
        if not client:
            return "OpenAIクライアントの初期化に失敗しました。"

        # メッセージの準備
        messages = [
            SystemMessage(content=system_prompt),
            *[
                HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
                for msg in chat_history[-5:]
            ],
            HumanMessage(content=user_input),
        ]

        # OpenAI APIに送信するためのメッセージ形式に変換
        api_messages = [
            {
                "role": (
                    "system"
                    if isinstance(msg, SystemMessage)
                    else "user" if isinstance(msg, HumanMessage) else "assistant"
                ),
                "content": msg.content,
            }
            for msg in messages
        ]

        # ストリーミングレスポンスの処理
        response_text = ""
        for chunk in client.chat.completions.create(
            messages=api_messages,
            model="gpt-4o-mini",
            temperature=0,
            stream=True,
        ):
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content
                if message_placeholder is not None:
                    message_placeholder.markdown(response_text + "▌")

        if message_placeholder is not None:
            message_placeholder.markdown(response_text)
        return response_text

    except Exception as e:
        error_msg = f"チャットレスポンスの取得中にエラーが発生しました: {str(e)}"
        st.error(error_msg)
        return error_msg


def show_chatbot_page():
    """チャットボット画面を表示"""
    # 現在のページがチャットボットでない場合は即座に終了
    if st.session_state.page != "chatbot":
        return

    # ログインチェック
    if not st.session_state.get("password_correct", False):
        st.error("ログインが必要です")
        st.stop()

    # OpenAIクライアントの初期化
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = get_openai_client()

    # メインコンテンツ
    st.title("QA Chatbot System")

    # システムプロンプトの読み込みとセッション状態への保存
    if "SYSTEM_PROMPTS" not in st.session_state:
        st.session_state.SYSTEM_PROMPTS = load_system_prompts()

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # カテゴリ選択の説明を追加
    st.markdown(
        """
    ### 使い方
    1. サイドバーからカテゴリを選択してください
    2. 質問を入力してください
    
    #### カテゴリの説明
    - 機能分類：音楽アプリの機能について質問できます
    - テスト分類：テストの分類方法について質問できます
    - 評価シート作成：テストケースの作成方法について質問できます
    """
    )

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    if user_input := st.chat_input("メッセージを入力してください"):
        # まずユーザー入力を表示とチャット履歴に追加
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            selected_category = st.session_state.get("chatbot_category")
            if selected_category:
                # システムプロンプトの準備
                system_prompt = st.session_state.SYSTEM_PROMPTS[selected_category]["content"]

                # アシスタントのメッセージ枠を準備
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    # ストリーミングで応答を取得・表示（チャット履歴も渡す）
                    response = get_chat_response(
                        system_prompt, user_input, message_placeholder, st.session_state.messages
                    )
                    # チャット履歴に追加
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("サイドバーからカテゴリを選択してください")

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    show_chatbot_page()
