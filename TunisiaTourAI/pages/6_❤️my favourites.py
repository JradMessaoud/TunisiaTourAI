import streamlit as st
from utils.favorites_manager import display_favorites_page
from utils.translate import translate_text

# Page configuration
st.set_page_config(
    page_title="❤️ My Favorites - TunisiaTourAI",
    page_icon="❤️",
    layout="wide"
)

# Minimal CSS for overall style (optional)
st.markdown("""
<style>
    .favorites-container {
        background: linear-gradient(135deg, #ffe0e0 0%, #ffd6d6 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #E70013;
        box-shadow: 0 4px 24px rgba(231,0,19,0.10);
    }
    @media (max-width: 600px) {
        .favorites-container {
            padding: 1rem !important;
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("## ❤️ My Favorites")
st.markdown("Find all your favorite places and itineraries in Tunisia")

# Display favorites page
display_favorites_page()

# Footer
st.markdown("---")
st.markdown("❤️ Favorites created with ❤️ for Tunisia by **Jrad Messaoud**")

# Ensure UI language state defaults to English
st.session_state.setdefault("lang", "en")
lang = st.session_state.get("lang", "en")
TEXTS = st.session_state.get('TEXTS', {})

