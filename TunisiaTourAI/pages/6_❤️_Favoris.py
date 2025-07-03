import streamlit as st
from utils.favorites_manager import display_favorites_page
from utils.translate import translate_text

# Configuration de la page
st.set_page_config(
    page_title="❤️ Mes Favoris - TunisiaTourAI",
    page_icon="❤️",
    layout="wide"
)

# CSS personnalisé pour les favoris
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
    .favorites-container h1 {
        color: #B3000F;
        font-size: 2.8rem;
        font-weight: 900;
        margin-bottom: 0.3rem;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px #fff, 0 2px 8px #E70013;
    }
    .favorites-container p {
        color: #B3000F;
        font-size: 1.2rem;
        opacity: 0.95;
        margin-top: 0;
        text-shadow: 0 1px 4px #fff;
    }
    .favorite-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #E70013;
        transition: transform 0.2s ease;
    }
    .favorite-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(231, 0, 19, 0.2);
    }
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #666;
    }
    .stats-card {
        background: linear-gradient(135deg, #E70013 0%, #B3000F 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("""
<div class="favorites-container">
    <h1>❤️ Mes Favoris</h1>
    <p>Retrouvez tous vos lieux et itinéraires préférés en Tunisie</p>
</div>
""", unsafe_allow_html=True)

# Affichage de la page des favoris
display_favorites_page()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>❤️ Favoris créés avec ❤️ pour la Tunisie par <strong>Jrad Messaoud</strong></p>
</div>
""", unsafe_allow_html=True)

# Après chaque génération de texte dynamique (ex: description IA, résumé IA, etc.)
st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

if lang != 'fr':
    texte = translate_text(texte, lang)
# st.markdown(texte) ou affichage équivalent 