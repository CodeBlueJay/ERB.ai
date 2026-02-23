
import os
import subprocess
import sys
import streamlit as st
from erb_logic import generate_response

def start_discord_bot_if_needed() -> None:
    if "discord_bot_started" in st.session_state and st.session_state.discord_bot_started:
        return
    bot_path = os.path.join(os.path.dirname(__file__), "discord_bot.py")
    env = os.environ.copy()
    st.session_state.discord_bot_process = subprocess.Popen(
        [sys.executable, bot_path],
        env=env
    )
    st.session_state.discord_bot_started = True

start_discord_bot_if_needed()

st.set_page_config(page_title="ERB.ai", page_icon="💀")
st.title("ERB.ai")
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    name = "ERB" if message["role"] == "assistant" else "You"
    with st.chat_message(message["role"]):
        st.markdown(f"**{name}**")
        st.write(message["content"])

user_input = st.chat_input("Speak to the ERB.ai")

if user_input:
    with st.chat_message("user"):
        st.markdown("**You**")
        st.write(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    response_text = generate_response(user_input)

    with st.chat_message("assistant"):
        st.markdown("**ERB**")
        st.write(response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )