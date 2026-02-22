import streamlit as st
import random

# --- Keyword dictionary ---
responses = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "yo", "wsg"],
        "replies": [
            "hi",
            "wsg",
            "wsp"
        ]
    },
    "glaze": {
        "keywords": ["cool", "goated"],
        "replies": [
            "glazeeeeee",
            "chat is this glaze",
            "balrighhh",
            "yessir",
            "fr",
            "ts is lowk peak"
        ]
    },
    "arson": {
        "keywords": ["arson"],
        "replies": [
            "fuck arson",
            "arson is ai",
            "bro arson bro",
            "FUCKING JEFF",
            "stfu"
        ]
    },
    "hate": {
        "keywords": ["lame", "hate", "mid", "gay", "sybau", "kys", "fuck"],
        "replies": [
            "pure hate",
            "bro this is pure hate",
            "balrighhh",
            "😭",
            "your just hating",
            "stfu",
            "holy hating",
            "fuck you"
        ]
    },
    "humor": {
        "keywords": ["lmao", "lol"],
        "replies": [
            "LMFAO",
            "lol",
            "💀",
            "😭"
        ]
    },
    "questions": {
        "keywords": ["do", "are", "is", "would"],
        "replies": [
            "yea",
            "nah",
            "FUCK NO 😭",
            "FUCK YEA",
            "uhh"
        ]
    },
    "gay": {
        "keywords": ["dick"],
        "replies": [
            "you dont have one",
            "oh fuck no",
            "pack it up yo",
            "wth",
            "fuck you"
        ]
    },
    "people": {
        "keywords": ["codebluejay", "lieand"],
        "replies": [
            "yo I know that guy",
            "that guy is lowk goated"
        ]
    }
}

# --- Streamlit UI ---
st.set_page_config(page_title="ERB.ai", page_icon="💀")

st.title("ERB.ai")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    name = "ERB" if message["role"] == "assistant" else "You"
    with st.chat_message(message["role"]):
        st.markdown(f"**{name}**")
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Speak to the ERB.ai")

if user_input:

    # Show User Message
    with st.chat_message("user"):
        st.markdown("**You**")
        st.write(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    defaults = [
        "fuh you talm bout",
        "tuff",
        "oh okay",
        "balrighhh",
        "thats lowkey real",
        "pack it up yo",
        "wth",
        "bro 😭",
        "uhh",
        "what"
    ]

    response_text = random.choice(defaults)

    # Keyword detection
    user_input_lower = user_input.lower()
    found = False

    for category in responses.values():
        for keyword in category["keywords"]:
            if keyword in user_input_lower.split():
                response_text = random.choice(category["replies"])
                found = True
                break
        if found:
            break

    # Show bot response immediately
    with st.chat_message("assistant"):
        st.markdown("**ERB**")
        st.write(response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )