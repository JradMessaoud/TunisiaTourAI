import streamlit as st
import json
from datetime import datetime, timedelta
from agents.ai_agent import AIAgent
from config import TUNISIAN_REGIONS, TRAVEL_TYPES, SEASONS, BUDGET_LEVELS
import uuid
from utils.translate import translate_text
from utils.favorites_manager import add_to_favorites_button

# Configuration de la page
st.set_page_config(
    page_title="🗺️ Planificateur de Voyage - TunisiaTourAI",
    page_icon="🗺️",
    layout="wide"
)

# CSS personnalisé pour le planificateur (NOUVEAU STYLE)
st.markdown("""
<style>
    .planner-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #E70013;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .planner-container h1, .planner-container p {
        color: #1E1E1E !important;
        text-shadow: none;
    }
    .itinerary-card {
        background: #fff;
        color: #1E1E1E;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1.5px solid #E70013;
        transition: box-shadow 0.2s, border 0.2s;
    }
    .itinerary-card:hover {
        box-shadow: 0 6px 24px rgba(231,0,19,0.10);
        border: 2px solid #B3000F;
    }
    .day-card {
        background: linear-gradient(135deg, #E70013 0%, #B3000F 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .budget-indicator {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .budget-warning {
        background: #ffc107;
        color: #212529;
    }
    .budget-danger {
        background: #dc3545;
        color: white;
    }
    /* Titres et sous-titres */
    h1, h2, h3, h4 {
        color: #E70013 !important;
        font-weight: bold !important;
        text-shadow: none !important;
    }
    /* Cartes d'exemples */
    .itinerary-card h4 {
        color: #B3000F !important;
        margin-bottom: 0.5rem;
    }
    .itinerary-card p, .itinerary-card li {
        color: #222 !important;
        font-size: 1rem;
        margin-bottom: 0.2rem;
    }
    /* Bordure plus douce */
    .itinerary-card {
        border: 1.5px solid #E70013;
    }
    /* Fond général plus doux */
    body, .stApp {
        background: #18191A !important;
    }
    @media (max-width: 600px) {
        .planner-container, .section-title, .glass-card, .process-card, .advantage-card, .footer-modern, .itinerary-card {
            padding: 1rem !important;
            font-size: 1rem !important;
        }
        .planner-container h1 {
            font-size: 1.5rem !important;
        }
        .glass-card h3, .section-title {
            font-size: 1.1rem !important;
        }
        .footer-modern {
            font-size: 0.9rem !important;
        }
        .stButton>button {
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

# Titre principal
st.markdown("""
<div class="planner-container">
    <h1>🗺️ Planificateur de Voyage en Tunisie</h1>
    <p>Créez votre itinéraire personnalisé avec l'aide de l'IA tunisienne</p>
</div>
""", unsafe_allow_html=True)

# Initialisation de l'agent IA
@st.cache_resource
def get_ai_agent():
    return AIAgent()

ai_agent = get_ai_agent()

# Sidebar pour les paramètres
st.sidebar.markdown("## ⚙️ Paramètres du Voyage")
st.sidebar.markdown("---")

# Sélection de la durée
duration = st.sidebar.slider("📅 Durée du séjour (jours)", 1, 21, 7)

# Sélection de la région
region = st.sidebar.selectbox(
    "🌍 Région principale",
    list(TUNISIAN_REGIONS.keys()),
    help="Choisissez la région que vous souhaitez explorer"
)

# Sélection du type de voyage
travel_type = st.sidebar.selectbox(
    "🎯 Type de voyage",
    list(TRAVEL_TYPES.keys()),
    help="Quel type d'expérience recherchez-vous ?"
)

# Sélection de la saison
season = st.sidebar.selectbox(
    "🌤️ Saison de voyage",
    list(SEASONS.keys()),
    help="Quand prévoyez-vous de voyager ?"
)

# Sélection du budget
budget_level = st.sidebar.selectbox(
    "💰 Niveau de budget",
    list(BUDGET_LEVELS.keys()),
    help="Quel est votre budget quotidien ?"
)

# Intérêts spécifiques
st.sidebar.markdown("### 🎨 Intérêts Spéciaux")
interests = st.sidebar.multiselect(
    "Sélectionnez vos centres d'intérêt :",
    ["Histoire", "Culture", "Gastronomie", "Nature", "Plage", "Aventure", "Shopping", "Photographie", "Architecture", "Traditions"],
    default=["Histoire", "Culture"]
)

# Informations supplémentaires
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informations Complémentaires")
travelers_count = st.sidebar.number_input("👥 Nombre de voyageurs", 1, 10, 2)
has_car = st.sidebar.checkbox("🚗 Location de voiture")
prefers_guided = st.sidebar.checkbox("👨‍🏫 Visites guidées")

# Variable pour suivre l'état de génération
if "itinerary_generated" not in st.session_state:
    st.session_state.itinerary_generated = False

# Bouton pour générer l'itinéraire
if st.sidebar.button("🚀 Générer l'Itinéraire", type="primary", key="generate_itinerary"):
    st.session_state.itinerary_generated = True

# Affichage conditionnel
if st.session_state.itinerary_generated:
    # Générer l'identifiant unique UNE SEULE FOIS par génération
    if "itinerary_unique_id" not in st.session_state:
        st.session_state.itinerary_unique_id = str(uuid.uuid4())
    unique_id = st.session_state.itinerary_unique_id
    with st.spinner("L'IA tunisienne planifie votre voyage..."):
        
        # Préparation des paramètres
        budget_info = BUDGET_LEVELS[budget_level]
        region_info = TUNISIAN_REGIONS[region]
        travel_info = TRAVEL_TYPES[travel_type]
        season_info = SEASONS[season]
        
        # Création du prompt pour l'IA
        prompt = f"""
        Créez un itinéraire de voyage détaillé pour la Tunisie avec les paramètres suivants :
        
        📅 Durée : {duration} jours
        🌍 Région : {region} ({{region_info['description']}})
        🎯 Type : {travel_type} ({{travel_info['description']}})
        🌤️ Saison : {season} ({{season_info['description']}})
        💰 Budget : {budget_level} ({{budget_info['daily_budget']}}€/jour)
        🎨 Intérêts : {', '.join(interests)}
        👥 Voyageurs : {travelers_count} personnes
        🚗 Voiture : {'Oui' if has_car else 'Non'}
        👨‍🏫 Visites guidées : {'Oui' if prefers_guided else 'Non'}
        
        Créez un planning jour par jour avec :
        1. Itinéraire détaillé pour chaque jour
        2. Lieux à visiter (destinations, monuments, festivals)
        3. Restaurants recommandés
        4. Conseils pratiques (transport, hébergement)
        5. Budget estimé par jour
        6. Conseils culturels et de sécurité
        7. Alternatives en cas de météo défavorable
        
        Répondez en français de manière structurée et engageante.
        """
        
        # Génération de l'itinéraire
        itinerary = ai_agent.ask(prompt)
        
        # Affichage du résultat
        st.markdown("## 🗺️ Votre Itinéraire Personnalisé")
        
        # Informations générales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📅 Durée", f"{{duration}} jours")
        
        with col2:
            st.metric("🌍 Région", region)
        
        with col3:
            st.metric("💰 Budget/jour", f"{{budget_info['daily_budget']}}€")
        
        with col4:
            total_budget = budget_info['daily_budget'] * duration
            st.metric("💰 Budget total", f"{{total_budget}}€")
        
        # Affichage de l'itinéraire
        st.markdown("### 📋 Planning Détaillé")
        st.markdown(f"""
        <div class="itinerary-card">
            {{itinerary.replace(chr(10), '<br>')}}
        </div>
        """, unsafe_allow_html=True)
        
        # Ajout du bouton favoris pour l'itinéraire
        item = {
            "id": unique_id,
            "name": f"Itinéraire {region} {duration}j {travel_type}",
            "description": itinerary,
            "location": region,
            "type": "itineraire"
        }
        add_to_favorites_button("itineraries", item, f"fav_{unique_id}")
        
        # Conseils supplémentaires
        st.markdown("### 💡 Conseils Supplémentaires")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🌤️ Météo en {{season_info['name']}} :**
            - {{season_info['description']}}
            
            **🎉 Festivals de la saison :**
            - {{', '.join(season_info['festivals'])}}
            """)
        
        with col2:
            st.markdown("""
            **🏨 Hébergement recommandé :**
            - {{budget_info['accommodation']}}
            
            **🚗 Transport :**
            - {{budget_info['transport']}}
            """)
        
        # Boutons d'action
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Sauvegarder l'Itinéraire", key=f"save_itinerary_{unique_id}"):
                st.success("Itinéraire sauvegardé ! (Fonctionnalité à implémenter)")
        
        with col2:
            if st.button("📤 Partager", key=f"share_itinerary_{unique_id}"):
                st.info("Lien de partage généré ! (Fonctionnalité à implémenter)")
        
        with col3:
            if st.button("🔄 Modifier", key=f"modify_itinerary_{unique_id}"):
                st.session_state.itinerary_generated = False
                del st.session_state["itinerary_unique_id"]
                st.rerun()

else:
    # Section d'exemples d'itinéraires
    st.markdown("## 🎯 Exemples d'Itinéraires Populaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏖️ Circuit Balnéaire (7 jours)</h4>
            <p><strong>Région :</strong> Nord et Centre</p>
            <p><strong>Destinations :</strong> Hammamet → Sousse → Monastir → Mahdia</p>
            <p><strong>Budget :</strong> Moyen (100€/jour)</p>
            <p><strong>Idéal pour :</strong> Familles, couples, détente</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏛️ Circuit Culturel (5 jours)</h4>
            <p><strong>Région :</strong> Nord</p>
            <p><strong>Destinations :</strong> Tunis → Carthage → Sidi Bou Saïd → Bizerte</p>
            <p><strong>Budget :</strong> Élevé (200€/jour)</p>
            <p><strong>Idéal pour :</strong> Histoire, architecture, culture</p>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏜️ Aventure Saharienne (10 jours)</h4>
            <p><strong>Région :</strong> Sud</p>
            <p><strong>Destinations :</strong> Tozeur → Djerba → Zarzis → Tataouine</p>
            <p><strong>Budget :</strong> Économique (50€/jour)</p>
            <p><strong>Idéal pour :</strong> Aventure, désert, traditions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🎉 Festival & Culture (14 jours)</h4>
            <p><strong>Région :</strong> Tout le pays</p>
            <p><strong>Destinations :</strong> Selon les festivals de la saison</p>
            <p><strong>Budget :</strong> Luxe (500€/jour)</p>
            <p><strong>Idéal pour :</strong> Festivals, expérience premium</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🗺️ Planificateur créé avec ❤️ pour la Tunisie par <strong>Jrad Messaoud</strong></p>
</div>
""", unsafe_allow_html=True)

st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

# Après chaque génération de texte dynamique (ex: suggestions IA, itinéraire, etc.)
if lang != 'fr':
    texte = translate_text(texte, lang)
# st.markdown(texte) ou affichage équivalent 