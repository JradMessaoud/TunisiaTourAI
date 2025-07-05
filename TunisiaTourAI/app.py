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
    initial_sidebar_state="expanded"
)

# --- CSS MODERNE ---
st.markdown("""
<style>
body, .stApp {
    background: #101014 !important;
    color: #fff !important;
}

/* HEADER */
.main-header-modern {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    background: linear-gradient(135deg, #E70013 0%, #B3000F 100%);
    border-radius: 20px;
    margin: 2rem 0 2.5rem 0;
    padding: 2.5rem 2rem 2rem 2rem;
    box-shadow: 0 8px 32px rgba(231,0,19,0.18);
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

/* SECTION */
.section-title {
    color: #fff;
    font-size: 2rem;
    font-weight: 800;
    margin: 2.5rem 0 1.2rem 0;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px #E70013;
}
.section-subtitle {
    color: #E70013;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* CARDS */
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
.glass-card p {
    color: #f3f3f3;
    font-size: 1.05rem;
    margin-bottom: 0.2rem;
}

/* BUTTONS */
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
.cta-btn:hover {
    background: linear-gradient(90deg, #B3000F 0%, #E70013 100%);
    box-shadow: 0 4px 32px #E70013cc;
    transform: translateY(-2px) scale(1.03);
}

/* PROCESS CARDS */
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
.process-card h4 {
    color: #E70013;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

/* ADVANTAGES */
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
.advantage-card h4 {
    color: #fff;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.advantage-card p {
    color: #f3f3f3;
}

/* FOOTER */
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

@media (max-width: 600px) {
    .main-header-modern, .section-title, .glass-card, .process-card, .advantage-card, .footer-modern, .favorites-container, .planner-container, .itinerary-card {
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    .main-header-modern h1, .favorites-container h1, .planner-container h1 {
        font-size: 1.5rem !important;
    }
    .glass-card h3, .section-title {
        font-size: 1.1rem !important;
    }
    .footer-modern {
        font-size: 0.9rem !important;
    }
    .stButton>button, .cta-btn {
        width: 100% !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }
    img, .stImage>img {
        max-width: 100% !important;
        height: auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- HEADER MODERNE AVEC LOGO ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = os.path.join("images", "logo tunisiaAI.png")
logo_base64 = get_base64_image(logo_path) if os.path.exists(logo_path) else None
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo TunisiaTourAI" style="height:80px; border-radius:16px; box-shadow:0 2px 8px rgba(0,0,0,0.08); margin-right:2rem; background:#fff;">' if logo_base64 else ''

st.markdown(f"""
<div class="main-header-modern" style="display: flex; align-items: center; justify-content: center; gap: 2rem;">
    {logo_html}
    <div class="header-content" style="text-align: left;">
        <h1 style="margin-bottom:0.2rem;">🇹🇳 TunisiaTourAI</h1>
        <p style="margin-top:0;">Votre guide intelligent pour découvrir la beauté et la richesse de la Tunisie</p>
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
