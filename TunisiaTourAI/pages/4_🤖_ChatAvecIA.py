import streamlit as st
from agents.ai_agent import AIAgent

st.session_state["lang"] = "fr"
lang = "fr"

st.title("🤖 Chat avec l'IA sur la Tunisie")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("Posez votre question sur la Tunisie :", "")

if st.button("Envoyer") and user_input:
    ai = AIAgent()
    response = ai.ask(user_input)
    st.session_state["chat_history"].append((user_input, response))

for q, r in reversed(st.session_state["chat_history"]):
    st.markdown(f"**Vous :** {q}")
    st.markdown(f"**TunisiaTourAI 🤖 :** {r}") 