# =============================
# インポート
# =============================
import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# =============================
# 初期設定
# =============================
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=api_key
)

# =============================
# 関数定義
# =============================
def get_system_prompt(expert: str) -> str:
    if expert == "健康アドバイザー":
        return "あなたは健康と生活習慣に詳しい専門家です。質問者の健康をサポートする視点で回答してください。"
    elif expert == "キャリアコンサルタント":
        return "あなたはキャリア相談のプロフェッショナルです。質問者の悩みに親身に答えてください。"
    elif expert == "ITエンジニア":
        return "あなたは経験豊富なITエンジニアです。技術的なアドバイスをわかりやすく伝えてください。"
    else:
        return "あなたは優秀なアシスタントAIです。親切に対応してください。"

def get_response(user_input: str, expert_type: str) -> str:
    system_prompt = get_system_prompt(expert_type)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = chat(messages)
    return response.content

# =============================
# Streamlit UI
# =============================
st.title("専門家AIチャット")

st.markdown("""
このアプリは、あなたの質問に対して選択した専門家の視点から回答してくれるAIチャットです。  
以下の手順で使ってください：

1. 専門家の種類を選んでください（例：健康、キャリア、IT）  
2. 質問を入力してください  
3. 送信ボタンを押すと、AIが専門家として回答します🧠✨
""")

expert_type = st.radio(
    "専門家を選んでください：",
    ("健康アドバイザー", "キャリアコンサルタント", "ITエンジニア")
)

user_input = st.text_input("質問を入力してください")

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("専門家が考え中...🤔"):
            answer = get_response(user_input, expert_type)
            st.success("AIからの回答：")
            st.write(answer)
