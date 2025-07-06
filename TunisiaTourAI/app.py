import streamlit as st
from agents.ai_agent import AIAgent
import os
from dotenv import load_dotenv
import base64
from utils.i18n import TEXTS

# Charger les variables d'environnement
load_dotenv()

# --- GESTION MONOLINGUE FRANÇAIS ---
st.session_state["lang"] = "fr"
lang = "fr"

# Configuration de la page
st.set_page_config(
    page_title="TunisiaTourAI - Guide Intelligent de la Tunisie",
    page_icon="🇹🇳",
    layout="wide",
    initial_sidebar_state="collapsed"  # Fermé par défaut sur mobile
)

# --- CSS MODERNE ET RESPONSIVE ---
st.markdown("""
<style>
body, .stApp {
    background: #101014 !important;
    color: #fff !important;
}

/* DÉTECTION MOBILE */
@media (max-width: 768px) {
    .stApp {
        padding: 0.5rem !important;
    }
    
    /* Correction des modals superposés */
    .stModal {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 90vw !important;
        max-height: 80vh !important;
        z-index: 9999 !important;
        background: #1a1a1a !important;
        border-radius: 15px !important;
        border: 2px solid #E70013 !important;
    }
    
    .stModal .modal-content {
        overflow-y: auto !important;
        padding: 15px !important;
        max-height: 70vh !important;
    }
    
    /* Boutons tactiles */
    .stButton > button {
        width: 100% !important;
        height: 44px !important;  /* Taille minimale tactile */
        margin: 5px 0 !important;
        font-size: 16px !important;  /* Évite le zoom sur iOS */
        border-radius: 22px !important;
    }
    
    /* Cards responsives */
    .glass-card {
        margin: 10px 0 !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    
    /* Images responsives */
    .stImage > img {
        width: 100% !important;
        height: auto !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar mobile */
    .css-1d391kg {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Navigation mobile */
    .main .block-container {
        padding: 0.5rem !important;
    }
}

/* HEADER RESPONSIVE FIX FINAL */
.main-header-modern {
    width: 100vw !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.2rem 0.5rem !important;
}

@media (max-width: 768px) {
    body, .stApp {
        overflow-x: hidden !important;
    }
    .main-header-modern {
        width: 98vw !important;
        max-width: 98vw !important;
        min-width: 0 !important;
        margin: 1rem auto !important;
        border-radius: 18px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 1rem 0.5rem !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
        background: linear-gradient(135deg, #E70013 0%, #B3000F 100%) !important;
    }
    .main-header-modern img {
        display: block;
        margin: 0 auto 0.5rem auto;
        max-width: 55vw !important;
        height: auto !important;
        border-radius: 12px !important;
    }
    .main-header-modern h1, .main-header-modern p {
        font-size: 1.05rem !important;
        word-break: break-word !important;
        white-space: normal !important;
        line-height: 1.2 !important;
        margin: 0.5rem 0 !important;
        max-width: 90vw !important;
        overflow-wrap: break-word !important;
        text-align: center !important;
    }
    .main-header-modern .header-content {
        max-width: 90vw !important;
        margin: 0 auto !important;
        text-align: center !important;
    }
}

.main-header-modern img {
    height: 90px;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    background: #fff;
}

.main-header-modern .header-content {
    text-align: left;
}

.main-header-modern h1 {
    color: #fff;
    font-size: 2.8rem;
    font-weight: 900;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px #B3000F;
}

.main-header-modern p {
    color: #fff;
    font-size: 1.25rem;
    opacity: 0.95;
    margin-top: 0;
    text-shadow: 0 1px 4px #B3000F;
}

/* SECTION RESPONSIVE */
.section-title {
    color: #fff;
    font-size: 2rem;
    font-weight: 800;
    margin: 2.5rem 0 1.2rem 0;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px #E70013;
}

@media (max-width: 768px) {
    .section-title {
        font-size: 1.5rem !important;
        margin: 1.5rem 0 1rem 0 !important;
        text-align: center !important;
    }
}

.section-subtitle {
    color: #E70013;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
    .section-subtitle {
        font-size: 1rem !important;
        text-align: center !important;
    }
}

/* CARDS RESPONSIVE */
.glass-card {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    box-shadow: 0 4px 32px rgba(231,0,19,0.10);
    border: 1.5px solid rgba(231,0,19,0.18);
    padding: 2rem 1.5rem 1.5rem 1.5rem;
    margin-bottom: 1.5rem;
    color: #fff;
    transition: box-shadow 0.2s, border 0.2s, background 0.2s;
    backdrop-filter: blur(4px);
}

@media (max-width: 768px) {
    .glass-card {
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 12px !important;
    }
}

.glass-card:hover {
    box-shadow: 0 8px 40px #E70013aa;
    border: 2px solid #E70013;
    background: rgba(255,255,255,0.13);
}

.glass-card h3 {
    color: #fff;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 8px #E70013;
}

@media (max-width: 768px) {
    .glass-card h3 {
        font-size: 1.1rem !important;
        text-align: center !important;
    }
}

.glass-card p {
    color: #f3f3f3;
    font-size: 1.05rem;
    margin-bottom: 0.2rem;
}

@media (max-width: 768px) {
    .glass-card p {
        font-size: 0.95rem !important;
        text-align: center !important;
    }
}

/* BUTTONS RESPONSIVE */
.cta-btn {
    background: linear-gradient(90deg, #E70013 0%, #B3000F 100%);
    color: #fff;
    font-weight: 700;
    font-size: 1.2rem;
    border: none;
    border-radius: 30px;
    padding: 0.9rem 2.5rem;
    margin-top: 1.2rem;
    box-shadow: 0 2px 16px #E70013aa;
    transition: background 0.2s, box-shadow 0.2s, transform 0.2s;
    cursor: pointer;
}

@media (max-width: 768px) {
    .cta-btn {
        width: 100% !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
        margin-top: 0.8rem !important;
        border-radius: 25px !important;
    }
}

.cta-btn:hover {
    background: linear-gradient(90deg, #B3000F 0%, #E70013 100%);
    box-shadow: 0 4px 32px #E70013cc;
    transform: translateY(-2px) scale(1.03);
}

/* PROCESS CARDS RESPONSIVE */
.process-card {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    border: 1.2px solid #E70013;
    color: #fff;
    padding: 1.2rem 1rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px #E7001340;
    text-align: center;
}

@media (max-width: 768px) {
    .process-card {
        padding: 1rem 0.8rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 10px !important;
    }
}

.process-card h4 {
    color: #E70013;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

@media (max-width: 768px) {
    .process-card h4 {
        font-size: 1rem !important;
    }
}

/* ADVANTAGES RESPONSIVE */
.advantage-card {
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    border: 1.2px solid #fff2;
    color: #fff;
    padding: 1.2rem 1rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px #E7001340;
    text-align: center;
}

@media (max-width: 768px) {
    .advantage-card {
        padding: 1rem 0.8rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 10px !important;
    }
}

.advantage-card h4 {
    color: #fff;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

@media (max-width: 768px) {
    .advantage-card h4 {
        font-size: 1rem !important;
    }
}

.advantage-card p {
    color: #f3f3f3;
}

@media (max-width: 768px) {
    .advantage-card p {
        font-size: 0.9rem !important;
    }
}

/* FOOTER RESPONSIVE */
.footer-modern {
    background: #18191A;
    color: #fff;
    text-align: center;
    padding: 2rem 1rem 1rem 1rem;
    margin-top: 3rem;
    border-radius: 16px;
    font-size: 1.1rem;
    opacity: 0.95;
}

@media (max-width: 768px) {
    .favorites-container, .planner-container, .itinerary-card {
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .favorites-container h1, .planner-container h1 {
        font-size: 1.5rem !important;
    }
    
    .glass-card h3, .section-title {
        font-size: 1.1rem !important;
    }
    
    .footer-modern {
        font-size: 0.9rem !important;
        padding: 1.5rem 0.8rem 0.8rem 0.8rem !important;
        margin-top: 2rem !important;
    }
}

/* GRILLE RESPONSIVE */
@media (max-width: 768px) {
    .stColumns {
        flex-direction: column !important;
    }
    
    .stColumns > div {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
}

/* SIDEBAR RESPONSIVE */
@media (max-width: 768px) {
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border-right: 2px solid #E70013 !important;
    }
    
    .css-1d391kg .sidebar-content {
        padding: 1rem 0.5rem !important;
    }
}

/* ANIMATIONS MOBILE */
@media (max-width: 768px) {
    .glass-card:hover {
        transform: none !important;  /* Désactiver les animations sur mobile */
    }
    
    .cta-btn:hover {
        transform: none !important;
    }
}

/* ACCESSIBILITÉ MOBILE */
@media (max-width: 768px) {
    /* Taille minimale pour les éléments tactiles */
    .stButton > button,
    .stSelectbox > div,
    .stTextInput > div {
        min-height: 44px !important;
    }
    
    /* Espacement pour éviter les clics accidentels */
    .stButton > button {
        margin: 8px 0 !important;
    }
    
    /* Focus visible */
    .stButton > button:focus,
    .stSelectbox > div:focus,
    .stTextInput > div:focus {
        outline: 2px solid #E70013 !important;
        outline-offset: 2px !important;
    }
}

.main-header-container {
    background: linear-gradient(135deg, #E70013 0%, #B3000F 100%);
    padding: 2rem;
    border-radius: 20px;
    margin: 2rem 0 2.5rem 0;
    box-shadow: 0 8px 32px rgba(231,0,19,0.18);
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 2rem;
}
.main-header-container img {
    height: 90px;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    background: #fff;
}
.main-header-container .header-content {
    text-align: left;
}
.main-header-container h1 {
    color: #fff;
    font-size: 2.8rem;
    font-weight: 900;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px #B3000F;
}
.main-header-container p {
    color: #fff;
    font-size: 1.25rem;
    opacity: 0.95;
    margin-top: 0;
    text-shadow: 0 1px 4px #B3000F;
}
@media (max-width: 600px) {
    .main-header-container {
        flex-direction: column !important;
        gap: 1rem !important;
        padding: 1rem !important;
        margin: 1rem 0 1.5rem 0 !important;
        text-align: center !important;
    }
    .main-header-container img {
        height: 60px !important;
        border-radius: 12px !important;
    }
    .main-header-container h1 {
        font-size: 1.5rem !important;
        text-align: center !important;
    }
    .main-header-container p {
        font-size: 1rem !important;
        text-align: center !important;
    }
}
</style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = os.path.join("images", "logo tunisiaAI.png")
logo_base64 = get_base64_image(logo_path) if os.path.exists(logo_path) else None
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="TunisiaTourAI Logo" style="height:90px; border-radius:18px; box-shadow:0 2px 12px rgba(0,0,0,0.12); background:#fff;" />' if logo_base64 else '<div style="width:90px;height:90px;background:#fff;border-radius:18px;"></div>'

# --- HEADER PRINCIPAL ---
st.markdown(f"""
<div class="main-header-container">
    {logo_html}
    <div class="header-content">
        <h1>TN<br>TunisiaTourAI</h1>
        <p>Votre guide intelligent pour découvrir la beauté et la richesse de la Tunisie</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar avec navigation
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("---")

# Statistiques dans la sidebar
st.sidebar.markdown("### 📊 Statistiques")
st.sidebar.markdown("**🏖️ Destinations :** 15 lieux")
st.sidebar.markdown("**🗿 Monuments :** 18 sites")
st.sidebar.markdown("**🎉 Festivals :** 19 événements")

# Informations pratiques
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informations")
st.sidebar.markdown("**🌍 Langue :** Français")
st.sidebar.markdown("**💰 Devise :** Dinar tunisien")
st.sidebar.markdown("**⏰ Fuseau :** UTC+1")

# Debug de la clé API
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Debug API Key")
st.sidebar.success("✅ Google API key configurée")
st.sidebar.info("🔑 Clé API : YOUR API KEY")

# Page principale
st.markdown(f"## {TEXTS['welcome'][lang]}")

# Introduction
st.markdown(f"""
<div class="stContainer">
    <h3>{TEXTS['intro_title'][lang]}</h3>
    <p>{TEXTS['intro_desc'][lang]}</p>
</div>
""", unsafe_allow_html=True)

# --- SECTION FONCTIONNALITÉS ---
st.markdown(f"<div class=\"section-title\">{TEXTS['features'][lang]}</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class=\"glass-card\"><h3>{TEXTS['dest'][lang]}</h3><p>{TEXTS['dest_desc'][lang]}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class=\"glass-card\"><h3>{TEXTS['mon'][lang]}</h3><p>{TEXTS['mon_desc'][lang]}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class=\"glass-card\"><h3>{TEXTS['fest'][lang]}</h3><p>{TEXTS['fest_desc'][lang]}</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class=\"glass-card\"><h3>{TEXTS['ai'][lang]}</h3><p>{TEXTS['ai_desc'][lang]}</p></div>", unsafe_allow_html=True)

# --- SECTION PROCESSUS ---
st.markdown("<div class=\"section-title\">🔄 Notre Processus</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class=\"process-card\"><h4>1. Découvrir</h4><p>Parcourez les destinations, monuments et festivals tunisiens.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class=\"process-card\"><h4>2. Planifier</h4><p>Créez votre itinéraire personnalisé avec l'IA.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class=\"process-card\"><h4>3. Explorer</h4><p>Profitez de conseils pratiques et d'astuces locales.</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class=\"process-card\"><h4>4. Discuter</h4><p>Interagissez avec l'IA pour des recommandations en temps réel.</p></div>", unsafe_allow_html=True)

# --- SECTION AVANTAGES ---
st.markdown("<div class=\"section-title\">🚀 Pourquoi choisir TunisiaTourAI ?</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class=\"advantage-card\"><h4>🇹🇳 100% Tunisie</h4><p>Une IA spécialisée sur la Tunisie, ses régions, sa culture et ses événements.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class=\"advantage-card\"><h4>💡 IA Moderne</h4><p>Propulsée par Gemini 2.5 Pro, rapide et précise.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class=\"advantage-card\"><h4>📱 Responsive</h4><p>Une expérience fluide sur mobile, tablette et desktop.</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class=\"advantage-card\"><h4>🔒 Sécurisé</h4><p>Respect de la vie privée et des données utilisateurs.</p></div>", unsafe_allow_html=True)

# --- SECTION CALL TO ACTION ---
st.markdown(f"<div class=\"section-title\">{TEXTS['cta_title'][lang]}</div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;">
    <a href="/ChatAvecIA" target="_self" style="
        display: inline-block;
        background: linear-gradient(90deg, #E70013 0%, #B3000F 100%);
        color: #fff;
        font-weight: 700;
        font-size: 1.2rem;
        border: none;
        border-radius: 30px;
        padding: 0.9rem 2.5rem;
        margin-top: 1.2rem;
        box-shadow: 0 2px 16px #E70013aa;
        text-decoration: none;
        transition: background 0.2s, box-shadow 0.2s, transform 0.2s;
        cursor: pointer;
        filter: drop-shadow(0 0 12px #E70013);
    " onmouseover="this.style.background='linear-gradient(90deg, #B3000F 0%, #E70013 100%)';this.style.transform='translateY(-2px) scale(1.03)';" onmouseout="this.style.background='linear-gradient(90deg, #E70013 0%, #B3000F 100%)';this.style.transform='none';">
        {TEXTS['cta'][lang]}
    </a>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer-modern">
    🇹🇳 TunisiaTourAI &copy; 2024 — Développé avec ❤️ par <strong>Jrad Messaoud</strong><br>
    <span style="font-size:0.95em; opacity:0.7;">{TEXTS['footer'][lang]}</span>
</div>
""", unsafe_allow_html=True)
