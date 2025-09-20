import streamlit as st
import os
import uuid
from datetime import datetime, timedelta
from agents.ai_agent import AIAgent
from config import TUNISIAN_REGIONS, TRAVEL_TYPES, SEASONS, BUDGET_LEVELS
from utils.translate import translate_text
from utils.favorites_manager import add_to_favorites_button

# Page configuration
st.set_page_config(
    page_title="🗺️ Travel Planner - TunisiaTourAI",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS for the planner
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
    h1, h2, h3, h4 {
        color: #E70013 !important;
        font-weight: bold !important;
        text-shadow: none !important;
    }
    .itinerary-card h4 {
        color: #B3000F !important;
        margin-bottom: 0.5rem;
    }
    .itinerary-card p, .itinerary-card li {
        color: #222 !important;
        font-size: 1rem;
        margin-bottom: 0.2rem;
    }
    .itinerary-card {
        border: 1.5px solid #E70013;
    }
    body, .stApp {
        background: #18191A !important;
    }
    @media (max-width: 600px) {
        .planner-container, .section-title, .itinerary-card, .day-card, .footer {
            padding: 1rem !important;
            font-size: 1rem !important;
        }
        .planner-container h1 {
            font-size: 1.5rem !important;
        }
        .section-title {
            font-size: 1.1rem !important;
        }
        .footer {
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

# Main title
st.markdown(
    """
<div class="planner-container">
    <h1>🗺️ Tunisia Travel Planner</h1>
    <p>Create a personalized itinerary with help from TunisiaTourAI</p>
</div>
""",
    unsafe_allow_html=True,
)

# Initialize AI agent (cached)
@st.cache_resource
def get_ai_agent():
    return AIAgent()

ai_agent = get_ai_agent()

# Sidebar settings
st.sidebar.markdown("## ⚙️ Travel Settings")
st.sidebar.markdown("---")

# Duration selection
duration = st.sidebar.slider("📅 Trip duration (days)", 1, 21, 7)

# Region selection
region = st.sidebar.selectbox(
    "🌍 Main region",
    list(TUNISIAN_REGIONS.keys()),
    help="Choose the main region you'd like to explore"
)

# Travel type selection
travel_type = st.sidebar.selectbox(
    "🎯 Travel style",
    list(TRAVEL_TYPES.keys()),
    help="What kind of experience are you looking for?"
)

# Season selection
season = st.sidebar.selectbox(
    "🌤️ Travel season",
    list(SEASONS.keys()),
    help="When do you plan to travel?"
)

# Budget selection
budget_level = st.sidebar.selectbox(
    "💰 Budget level",
    list(BUDGET_LEVELS.keys()),
    help="What's your approximate daily budget?"
)

# Special interests
st.sidebar.markdown("### 🎨 Special interests")
interests = st.sidebar.multiselect(
    "Select your interests:",
    ["History", "Culture", "Gastronomy", "Nature", "Beach", "Adventure", "Shopping", "Photography", "Architecture", "Traditions"],
    default=["History", "Culture"],
)

# Additional info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Additional info")
travelers_count = st.sidebar.number_input("👥 Number of travelers", 1, 10, 2)
has_car = st.sidebar.checkbox("🚗 Car rental")
prefers_guided = st.sidebar.checkbox("👨‍🏫 Guided tours")

# Track generation state
st.session_state.setdefault("itinerary_generated", False)

# Generate itinerary button
if st.sidebar.button("🚀 Generate Itinerary", type="primary", key="generate_itinerary"):
    st.session_state.itinerary_generated = True

# If generated, create and display itinerary
if st.session_state.itinerary_generated:
    # Generate unique id once per generation
    st.session_state.setdefault("itinerary_unique_id", str(uuid.uuid4()))
    unique_id = st.session_state.itinerary_unique_id

    with st.spinner("TunisiaTourAI is planning your trip..."):
        # Prepare parameters
        budget_info = BUDGET_LEVELS[budget_level]
        region_info = TUNISIAN_REGIONS[region]
        travel_info = TRAVEL_TYPES[travel_type]
        season_info = SEASONS[season]

        # Build AI prompt
        prompt = f"""
Create a detailed day-by-day travel itinerary for Tunisia with the following parameters:

Duration: {duration} days
Region: {region} ({region_info.get('description','')})
Style: {travel_type} ({travel_info.get('description','')})
Season: {season} ({season_info.get('description','')})
Budget: {budget_level} ({budget_info.get('daily_budget','')}€/day)
Interests: {', '.join(interests)}
Travelers: {travelers_count}
Car rental: {'Yes' if has_car else 'No'}
Guided tours: {'Yes' if prefers_guided else 'No'}

Please produce:
1) A day-by-day plan with activities and approximate timings
2) Places to visit (destinations, monuments, festivals)
3) Recommended restaurants
4) Practical tips (transport, accommodation)
5) Estimated daily budget
6) Cultural & safety tips
7) Weather contingency alternatives

Respond in English, structured and engaging.
"""

        itinerary = ai_agent.ask(prompt)

        # If UI language differs, translate generated text
        ui_lang = st.session_state.get("lang", "en")
        if ui_lang != 'en':
            try:
                itinerary = translate_text(itinerary, ui_lang)
            except Exception:
                # fallback: keep original
                pass

        # Display results
        st.markdown("## 🗺️ Your Personalized Itinerary")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📅 Duration", f"{duration} days")
        with col2:
            st.metric("🌍 Region", region)
        with col3:
            st.metric("💰 Budget/day", f"{budget_info.get('daily_budget','')}€")
        with col4:
            total_budget = budget_info.get('daily_budget', 0) * duration
            st.metric("💰 Total budget", f"{total_budget}€")

        st.markdown("### 📋 Detailed Plan")
        st.markdown(f"<div class=\"itinerary-card\">{itinerary.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

        # Favorite button for itinerary
        item = {
            "id": unique_id,
            "name": f"Itinerary {region} {duration}d {travel_type}",
            "description": itinerary,
            "location": region,
            "type": "itinerary",
        }
        add_to_favorites_button("itineraries", item, f"fav_{unique_id}")

        # Additional tips
        st.markdown("### 💡 Additional Tips")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🌤️ Weather in {season_info.get('name', season)} :**\n- {season_info.get('description','')}\n\n**🎉 Seasonal festivals :**\n- {', '.join(season_info.get('festivals', []))}")
        with col2:
            st.markdown(f"**🏨 Recommended accommodation :**\n- {budget_info.get('accommodation','N/A')}\n\n**🚗 Transport :**\n- {budget_info.get('transport','N/A')}")

        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Itinerary", key=f"save_itinerary_{unique_id}"):
                st.success("Itinerary saved! (Functionality to implement)")
        with col2:
            if st.button("📤 Share", key=f"share_itinerary_{unique_id}"):
                st.info("Share link generated! (Functionality to implement)")
        with col3:
            if st.button("🔄 Modify", key=f"modify_itinerary_{unique_id}"):
                st.session_state['itinerary_generated'] = False
                if 'itinerary_unique_id' in st.session_state:
                    del st.session_state['itinerary_unique_id']
                st.experimental_rerun()

else:
    # Example itineraries
    st.markdown("## 🎯 Popular Example Itineraries")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏖️ Coastal Circuit (7 days)</h4>
            <p><strong>Region:</strong> North & Center</p>
            <p><strong>Destinations:</strong> Hammamet → Sousse → Monastir → Mahdia</p>
            <p><strong>Budget:</strong> Mid (100€/day)</p>
            <p><strong>Ideal for:</strong> Families, couples, relaxation</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏛️ Cultural Circuit (5 days)</h4>
            <p><strong>Region:</strong> North</p>
            <p><strong>Destinations:</strong> Tunis → Carthage → Sidi Bou Said → Bizerte</p>
            <p><strong>Budget:</strong> High (200€/day)</p>
            <p><strong>Ideal for:</strong> History, architecture, culture</p>
        </div>
        """, unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🏜️ Saharan Adventure (10 days)</h4>
            <p><strong>Region:</strong> South</p>
            <p><strong>Destinations:</strong> Tozeur → Djerba → Zarzis → Tataouine</p>
            <p><strong>Budget:</strong> Budget (50€/day)</p>
            <p><strong>Ideal for:</strong> Adventure, desert, traditions</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="itinerary-card">
            <h4>🎉 Festival & Culture (14 days)</h4>
            <p><strong>Region:</strong> Nationwide</p>
            <p><strong>Destinations:</strong> According to seasonal festivals</p>
            <p><strong>Budget:</strong> Luxury (500€/day)</p>
            <p><strong>Ideal for:</strong> Festivals, premium experiences</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🗺️ Planner crafted with ❤️ for Tunisia by <strong>Jrad Messaoud</strong></p>
</div>
""", unsafe_allow_html=True)

# Ensure UI language state defaults to English
st.session_state.setdefault("lang", "en")

# Note: If you want to translate dynamic texts later, use translate_text() where needed.
