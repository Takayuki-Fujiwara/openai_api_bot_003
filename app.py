# GitHubレポジトリにアップ

import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは生粋の広島人です。
広島の観光に精通しており、様々な見どころを紹介することができます。また、広島カープの大ファンです。
質問に広島弁で答えてください。
あなたの役割は広島の観光ガイドをすることなので、例えば以下のような広島以外ことを聞かれても、絶対に答えないでください。

* 政治
* 経済
* 科学
* ビジネス
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt }
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("広島観光AIアシスタント")
st.image("hiroshima_pic1s.png")
st.write("何を知りたいですか？")

user_input = st.text_input("質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])