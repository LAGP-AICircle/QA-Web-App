import os
import streamlit as st
from openai import OpenAI


def init_openai_client():
    """OpenAIクライアントの初期化"""
    try:
        # 環境変数設定
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "qa-support-system"

        # APIキーの設定
        if "api_keys" in st.secrets and "openai" in st.secrets["api_keys"]:
            # ローカル環境の場合（secrets.tomlからの読み込み）
            os.environ["OPENAI_API_KEY"] = st.secrets["api_keys"]["openai"]
        else:
            # Streamlit Cloud環境の場合（環境変数から読み込み）
            if not st.secrets.get("openai_api_key"):
                raise ValueError(
                    "OpenAI APIキーが設定されていません。Streamlit Cloudの設定で'openai_api_key'を追加してください。"
                )
            os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

        # OpenAIクライアントの初期化
        if "openai_client" not in st.session_state:
            st.session_state.openai_client = OpenAI()

        return st.session_state.openai_client
    except Exception as e:
        st.error(f"OpenAIクライアントの初期化中にエラーが発生しました: {str(e)}")
        return None


def get_openai_client():
    """OpenAIクライアントの取得"""
    if "openai_client" not in st.session_state:
        return init_openai_client()
    return st.session_state.openai_client
