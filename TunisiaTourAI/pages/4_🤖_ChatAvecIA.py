import streamlit as st
from agents.ai_agent import AIAgent

# Set language & TEXTS
st.session_state.setdefault("lang", "en")
lang = st.session_state["lang"]
TEXTS = st.session_state.get("TEXTS", {})

# Fallback labels (safe lookups)
title = TEXTS.get("chat_title", {}).get(lang, "🤖 Chat with TunisiaTourAI")
prompt_label = TEXTS.get("chat_prompt", {}).get(lang, "Ask your question about Tunisia:")
send_label = TEXTS.get("chat_send", {}).get(lang, "Send")
you_label = TEXTS.get("you_label", {}).get(lang, "You")
ai_label = TEXTS.get("ai_label", {}).get(lang, "TunisiaTourAI 🤖")

st.title(title)

# Initialize history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input field (clears after sending)
user_input = st.text_input(prompt_label, key="user_input")

if st.button(send_label) and user_input:
    ai = AIAgent()
    response = ai.ask(user_input)
    st.session_state["chat_history"].append((user_input, response))
    # clear input box
    st.session_state["user_input"] = ""

# Display chat history (most recent first)
for q, r in reversed(st.session_state["chat_history"]):
    st.markdown(f"**{you_label} :** {q}")
    st.markdown(f"**{ai_label} :** {r}")
