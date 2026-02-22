import streamlit as st
import random
import re
from rapidfuzz import fuzz

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
        "keywords": ["cool", "goated", "glaze"],
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
        "keywords": ["do", "is", "would", "can", "are you"],
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
    },
    "jason": {
        "keywords": ["jason singh"],
        "replies": [
            "jason singh is strange"
        ]
    },
    "blm": {
        "keywords": ["blm"],
        "replies": [
            "yea i support blm"
        ]
    },
    "clanker": {
        "keywords": ["clanker"],
        "replies": [
            "who is ts guy calling a clanker"
        ]
    }
    "niceness": {
        "keywords": ["hru", "how are you", "how you doin", "you good"],
        "replies": [
            "im chillin",
            "im good fr",
            "yea im straight",
            "we good"
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
    user_input_clean = re.sub(r"[^\w\s]", "", user_input_lower)
    user_words = user_input_clean.split()
    found = False
    fuzzy_match_threshold = 85

    for category in responses.values():
        for keyword in category["keywords"]:
            if keyword in user_words:
                response_text = random.choice(category["replies"])
                found = True
                break
        if found:
            break

    if not found:
        best_score = 0
        best_category = None

        for category in responses.values():
            for keyword in category["keywords"]:
                if " " in keyword:
                    score = fuzz.partial_ratio(keyword, user_input_clean)
                else:
                    score = max((fuzz.ratio(keyword, word) for word in user_words), default=0)

                if score > best_score:
                    best_score = score
                    best_category = category

        if best_category and best_score >= fuzzy_match_threshold:
            response_text = random.choice(best_category["replies"])
            found = True

    # Show bot response immediately
    with st.chat_message("assistant"):
        st.markdown("**ERB**")
        st.write(response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )