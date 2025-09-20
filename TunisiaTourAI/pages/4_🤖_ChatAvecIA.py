import streamlit as st
from agents.ai_agent import AIAgent

# Set default language to English
st.session_state.setdefault("lang", "en")
lang = st.session_state["lang"]

st.title("🤖 Chat with TunisiaTourAI")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

ai = AIAgent()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question about Tunisia:", "")
    submit = st.form_submit_button("Send")

    if submit and user_input:
        response = ai.ask(user_input)
        st.session_state["chat_history"].append((user_input, response))

for q, r in reversed(st.session_state["chat_history"]):
    st.markdown(f"**You :** {q}")
    st.markdown(f"**TunisiaTourAI 🤖 :** {r}")
