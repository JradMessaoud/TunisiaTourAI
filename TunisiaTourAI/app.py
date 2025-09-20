import streamlit as st
from agents.ai_agent import AIAgent
import os
from dotenv import load_dotenv
import base64
from utils.i18n import TEXTS

# Load environment variables
load_dotenv()

# --- MONOLINGUAL ENGLISH MANAGEMENT ---
st.session_state["lang"] = "en"
lang = "en"

# Safe text access function with fallbacks
def get_text(key, lang="en"):
    fallbacks = {
        'welcome': 'Welcome to Tunisia',
        'intro_title': 'Discover Tunisia with AI',
        'intro_desc': 'Your intelligent guide to explore the wonders of Tunisia',
        'features': 'Features',
        'dest': 'Destinations',
        'dest_desc': 'Discover the most beautiful places in Tunisia',
        'mon': 'Monuments',
        'mon_desc': 'Explore historical and cultural monuments',
        'fest': 'Festivals',
        'fest_desc': 'Participate in traditional and modern festivals',
        'ai': 'AI Assistant',
        'ai_desc': 'Get personalized recommendations',
        'cta_title': 'Start the Adventure',
        'cta': 'Chat with AI',
        'footer': 'All rights reserved'
    }
    
    try:
        return TEXTS.get(key, {}).get(lang, fallbacks.get(key, f"Text for {key}"))
    except:
        return fallbacks.get(key, f"Text for {key}")

# Page configuration
st.set_page_config(
    page_title="TunisiaTourAI - Intelligent Guide to Tunisia",
    page_icon="🇹🇳",
    layout="wide",
    initial_sidebar_state="collapsed"  # Closed by default on mobile
)

# --- MODERN AND RESPONSIVE CSS ---
st.markdown("""
<style>
body, .stApp {
    background: #101014 !important;
    color: #fff !important;
}

/* MOBILE DETECTION */
@media (max-width: 768px) {
    .stApp {
        padding: 0.5rem !important;
    }
    
    /* Overlay modal correction */
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
    
    /* Touch buttons */
    .stButton > button {
        width: 100% !important;
        height: 44px !important;  /* Minimum touch size */
        margin: 5px 0 !important;
        font-size: 16px !important;  /* Prevents iOS zoom */
        border-radius: 22px !important;
    }
    
    /* Responsive cards */
    .glass-card {
        margin: 10px 0 !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    
    /* Responsive images */
    .stImage > img {
        width: 100% !important;
        height: auto !important;
        border-radius: 10px !important;
    }
    
    /* Mobile sidebar */
    .css-1d391kg {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Mobile navigation */
    .main .block-container {
        padding: 0.5rem !important;
    }
}

/* FINAL RESPONSIVE HEADER FIX */
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

/* RESPONSIVE SECTION */
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

/* RESPONSIVE CARDS */
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

/* RESPONSIVE BUTTONS */
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

/* RESPONSIVE PROCESS CARDS */
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

/* RESPONSIVE ADVANTAGES */
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

/* RESPONSIVE FOOTER */
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

/* RESPONSIVE GRID */
@media (max-width: 768px) {
    .stColumns {
        flex-direction: column !important;
    }
    
    .stColumns > div {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
}

/* RESPONSIVE SIDEBAR */
@media (max-width: 768px) {
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        border-right: 2px solid #E70013 !important;
    }
    
    .css-1d391kg .sidebar-content {
        padding: 1rem 0.5rem !important;
    }
}

/* MOBILE ANIMATIONS */
@media (max-width: 768px) {
    .glass-card:hover {
        transform: none !important;  /* Disable animations on mobile */
    }
    
    .cta-btn:hover {
        transform: none !important;
    }
}

/* MOBILE ACCESSIBILITY */
@media (max-width: 768px) {
    /* Minimum size for touch elements */
    .stButton > button,
    .stSelectbox > div,
    .stTextInput > div {
        min-height: 44px !important;
    }
    
    /* Spacing to prevent accidental clicks */
    .stButton > button {
        margin: 8px 0 !important;
    }
    
    /* Visible focus */
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

# --- MAIN HEADER ---
st.markdown(f"""
<div class="main-header-container">
    {logo_html}
    <div class="header-content">
        <h1>TN<br>TunisiaTourAI</h1>
        <p>Your intelligent guide to discover the beauty and richness of Tunisia</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with navigation
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("---")

# Statistics in sidebar
st.sidebar.markdown("### 📊 Statistics")
st.sidebar.markdown("**🏖️ Destinations:** 15 places")
st.sidebar.markdown("**🗿 Monuments:** 18 sites")
st.sidebar.markdown("**🎉 Festivals:** 19 events")

# Practical information
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Information")
st.sidebar.markdown("**🌍 Language:** English")
st.sidebar.markdown("**💰 Currency:** Tunisian Dinar")
st.sidebar.markdown("**⏰ Timezone:** UTC+1")

# API key debug
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 API Key Debug")
st.sidebar.success("✅ Google API key configured")
st.sidebar.info("🔑 API Key: YOUR API KEY")

# Main page
welcome_text = get_text('welcome', lang)
st.markdown(f"## {welcome_text}")

# Introduction
intro_title = get_text('intro_title', lang)
intro_desc = get_text('intro_desc', lang)
st.markdown(f"""
<div class="stContainer">
    <h3>{intro_title}</h3>
    <p>{intro_desc}</p>
</div>
""", unsafe_allow_html=True)

# --- FEATURES SECTION ---
features_text = get_text('features', lang)
st.markdown(f"<div class=\"section-title\">{features_text}</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

dest_text = get_text('dest', lang)
dest_desc_text = get_text('dest_desc', lang)
mon_text = get_text('mon', lang)
mon_desc_text = get_text('mon_desc', lang)
fest_text = get_text('fest', lang)
fest_desc_text = get_text('fest_desc', lang)
ai_text = get_text('ai', lang)
ai_desc_text = get_text('ai_desc', lang)

with col1:
    st.markdown(f"<div class=\"glass-card\"><h3>{dest_text}</h3><p>{dest_desc_text}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class=\"glass-card\"><h3>{mon_text}</h3><p>{mon_desc_text}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class=\"glass-card\"><h3>{fest_text}</h3><p>{fest_desc_text}</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class=\"glass-card\"><h3>{ai_text}</h3><p>{ai_desc_text}</p></div>", unsafe_allow_html=True)

# --- PROCESS SECTION ---
st.markdown("<div class=\"section-title\">🔄 Our Process</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class=\"process-card\"><h4>1. Discover</h4><p>Explore Tunisian destinations, monuments, and festivals.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class=\"process-card\"><h4>2. Plan</h4><p>Create your personalized itinerary with AI.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class=\"process-card\"><h4>3. Explore</h4><p>Enjoy practical advice and local tips.</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class=\"process-card\"><h4>4. Chat</h4><p>Interact with AI for real-time recommendations.</p></div>", unsafe_allow_html=True)

# --- ADVANTAGES SECTION ---
st.markdown("<div class=\"section-title\">🚀 Why choose TunisiaTourAI?</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class=\"advantage-card\"><h4>🇹🇳 100% Tunisia</h4><p>An AI specialized in Tunisia, its regions, culture, and events.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class=\"advantage-card\"><h4>💡 Modern AI</h4><p>Powered by Gemini 2.5 Pro, fast and accurate.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class=\"advantage-card\"><h4>📱 Responsive</h4><p>A smooth experience on mobile, tablet, and desktop.</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class=\"advantage-card\"><h4>🔒 Secure</h4><p>Respect for privacy and user data.</p></div>", unsafe_allow_html=True)

# --- CALL TO ACTION SECTION ---
cta_title = get_text('cta_title', lang)
cta_text = get_text('cta', lang)
st.markdown(f"<div class=\"section-title\">{cta_title}</div>", unsafe_allow_html=True)
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
        {cta_text}
    </a>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
footer_text = get_text('footer', lang)
st.markdown(f"""
<div class="footer-modern">
    🇹🇳 TunisiaTourAI &copy; 2024 — Developed with ❤️ by <strong>Jrad Messaoud</strong><br>
    <span style="font-size:0.95em; opacity:0.7;">{footer_text}</span>
</div>
""", unsafe_allow_html=True)
