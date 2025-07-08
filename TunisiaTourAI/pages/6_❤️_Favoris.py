import streamlit as st
from utils.favorites_manager import display_favorites_page
from utils.translate import translate_text

# Configuration de la page
st.set_page_config(
    page_title="❤️ Mes Favoris - TunisiaTourAI",
    page_icon="❤️",
    layout="wide"
)

# CSS minimal pour le style général (optionnel, à garder si besoin)
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

# Titre principal en markdown natif
st.markdown("## ❤️ Mes Favoris")
st.markdown("Retrouvez tous vos lieux et itinéraires préférés en Tunisie")

# Affichage de la page des favoris
display_favorites_page()

# Footer natif
st.markdown("---")
st.markdown("❤️ Favoris créés avec ❤️ pour la Tunisie par **Jrad Messaoud**")

# Après chaque génération de texte dynamique (ex: description IA, résumé IA, etc.)
st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

if lang != 'fr':
    texte = translate_text(texte, lang)
# st.markdown(texte) ou affichage équivalent 
