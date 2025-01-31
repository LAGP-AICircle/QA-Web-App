import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import os
import openai
from langsmith import wrappers, traceable
from auth import check_password

# ページ設定
st.set_page_config(page_title="QA事業部 専属チャットボット", page_icon=":speech_balloon:", layout="wide")

# LangSmith設定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["api_keys"]["langsmith"]
os.environ["LANGCHAIN_PROJECT"] = "qa-support-system"
os.environ["OPENAI_API_KEY"] = st.secrets["api_keys"]["openai"]

# OpenAIクライアントのラップ
client = wrappers.wrap_openai(openai.Client())


# システムプロンプトの読み込み
def load_system_prompts():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(current_dir, "prompts", "system_prompts.json")
    with open(prompts_path, "r", encoding="utf-8") as f:
        return json.load(f)


#@traceable
def _get_chat_completion(messages: list, temperature: float = 0) -> str:
    """OpenAI APIを使用してチャット応答を取得（非ストリーミング）"""
    try:
        response = client.chat.completions.create(
            messages=messages, model="gpt-4o-mini", temperature=temperature, stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


#@traceable
def prepare_messages(system_prompt: str, user_input: str, chat_history: list) -> list:
    """チャットメッセージの準備"""
    return [
        {"role": "system", "content": system_prompt},
        *[{"role": msg["role"], "content": msg["content"]} for msg in chat_history[-5:]],
        {"role": "user", "content": user_input},
    ]

def get_chat_response(system_prompt: str, user_input: str, message_placeholder, chat_history: list) -> str:
    """ストリーミング対応のチャット応答を取得"""
    try:
        messages = prepare_messages(system_prompt, user_input, chat_history)

        # ストリーミングレスポンスの処理
        response_text = ""
        for chunk in client.chat.completions.create(
            messages=messages,
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

def main():
    # ログインチェックを追加
    if not check_password():
        return # ログインしていない場合は、ここで処理を終了
    
    st.title("QA Support System")

    # システムプロンプトの読み込み
    SYSTEM_PROMPTS = load_system_prompts()

    # サイドバー
    with st.sidebar:
        st.title("Options")
        selected_category = st.selectbox("カテゴリを選択してください", options=list(SYSTEM_PROMPTS.keys()))

        if st.button("Logout"):
           del st.session_state["password_correct"]
           del st.session_state["logged_in_email"]
           st.rerun()

        # 会話履歴クリアボタン
        if st.button("会話履歴をクリア"):
            st.session_state.messages = []
            st.rerun()

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
            # システムプロンプトの準備
            system_prompt = SYSTEM_PROMPTS[selected_category]["base_instruction"]
            if selected_category == "機能分類":
                system_prompt += f"\n\n分類体系:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['classification_structure'], ensure_ascii=False, indent=2)}"
                system_prompt += f"\n\n機能ツリー:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['function_tree'], ensure_ascii=False, indent=2)}"
                system_prompt += "\n\n以下は回答例です：\n"
                for example in SYSTEM_PROMPTS[selected_category]["few_shot_examples"].values():
                    system_prompt += f"\n質問：{example['question']}\n\n回答：\n{example['answer']}\n"
            elif selected_category == "テスト分類":
                system_prompt += f"\n\nテスト分類詳��:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['test_classification'], ensure_ascii=False, indent=2)}"
                system_prompt += "\n\n以下は回答例です：\n"
                for example in SYSTEM_PROMPTS[selected_category]["few_shot_examples"].values():
                    system_prompt += f"\n質問：{example['question']}\n\n回答：\n{example['answer']}\n"
            elif selected_category == "評価シート":
                system_prompt += f"\n\n評価シートの文脈:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['context'], ensure_ascii=False, indent=2)}"
                system_prompt += f"\n\n評価項目:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['items'], ensure_ascii=False, indent=2)}"
                system_prompt += f"\n\n評価シート例:\n{json.dumps(SYSTEM_PROMPTS[selected_category]['Example'], ensure_ascii=False, indent=2)}"

            # アシスタントのメッセージ枠を準備
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                # ストリーミングで応答を取得・表示（チャット履歴も渡す）
                response = get_chat_response(system_prompt, user_input, message_placeholder, st.session_state.messages)
                # チャット履歴に追加
                st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
