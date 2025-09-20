import streamlit as st
import os
from agents.ai_agent import AIAgent
from utils.favorites_manager import add_to_favorites_button
from utils.mobile_utils import get_responsive_columns, responsive_image_display, optimize_for_mobile

# Mobile optimizations
optimize_for_mobile()

# Language / texts
st.session_state["lang"] = "en"
lang = "en"
TEXTS = st.session_state.get('TEXTS', {})

# Cached labels / fallbacks
title_text = TEXTS.get('mon_title', {}).get(lang, '🏛️ Historic Monuments of Tunisia')
city_label = TEXTS.get('city_label', {}).get(lang, 'City / Region')
all_cities_label = TEXTS.get('all_cities', {}).get(lang, 'All')
img_not_found_text = TEXTS.get('img_not_found', {}).get(lang, 'Image not found')
no_mon_text = TEXTS.get('no_mon', {}).get(lang, 'No monuments found for this city/region.')
ai_explain_label = TEXTS.get('ai_explain', {}).get(lang, 'AI explanation for')
ai_explain_loading = TEXTS.get('ai_explain_loading', {}).get(lang, 'Generating AI explanation...')
stats_label = TEXTS.get('stats', {}).get(lang, 'Statistics')
total_label = TEXTS.get('total', {}).get(lang, 'Total')
shown_label = TEXTS.get('shown', {}).get(lang, 'Shown')
monuments_label = TEXTS.get('monuments', {}).get(lang, 'monuments')
must_see_label = TEXTS.get('must_see', {}).get(lang, 'Must-see monument')
ai_recommend_loading = TEXTS.get('ai_recommend_loading', {}).get(lang, 'Generating recommendation...')

st.title(title_text)

# Mapping monuments to local images
MONUMENT_IMAGES = {
    "El Jem Colosseum": "Amphi_El_Jem.jpg",
    "Okba Mosque": "800px-Grande_Mosquée_de_Kairouan,_vue_d'ensemble.jpg",
    "Carthage Site": "Carthage.JPG",
    "Dougga": "Dougga.jpg",
    "Monastir Ribat": "MONASTIR_RIBAT.jpg",
    "Tunis Medina": "medina_tunis.jpg",
    "Sousse Medina": "MEDINA OF SOUSSE.jpg",
    "Sfax Medina": "MEDINA OF _Sfax.jpg",
    "Bourguiba Mausoleum": "bourguiba_mausoleum.jpg",
    "Saint-Louis Cathedral": "CATHEDRAL SAINT LOUIS CARTHAGE.jpg",
    "Kelibia Fort": "Fort_de_kelibia_3.jpg",
    "Kef Citadel": "KEF CITADELLE.jpg",
    "Zitouna Mosque": "zitouna.jpg",
    "Bizerte Port": "port_de_BIZERTE-Tunisie.jpg",
    "Bulla Regia Site": "bulla_regia.jpg",
    "Thuburbo Majus Site": "thuburbo_majus.jpg",
    "Testour Medina": "Testour.jpg",
    "Makthar Site": "MAKTHAR.jpg"
}

# Monuments data (English keys and descriptions)
MONUMENTS = [
    {
        "name": "El Jem Colosseum",
        "city": "El Jem",
        "image": MONUMENT_IMAGES["El Jem Colosseum"],
        "description": "An impressive Roman amphitheatre listed as a UNESCO World Heritage site. It is the third-largest amphitheatre of the Roman world after Rome and Capua."
    },
    {
        "name": "Okba Mosque",
        "city": "Kairouan",
        "image": MONUMENT_IMAGES["Okba Mosque"],
        "description": "One of the oldest and most prestigious mosques in the Muslim world. It is a spiritual center of Islam in North Africa and a major historic religious site."
    },
    {
        "name": "Carthage Site",
        "city": "Carthage",
        "image": MONUMENT_IMAGES["Carthage Site"],
        "description": "Ancient ruins of a legendary city that was the center of Carthaginian civilization. A UNESCO World Heritage site bearing witness to Punic and Roman history."
    },
    {
        "name": "Dougga",
        "city": "Téboursouk",
        "image": MONUMENT_IMAGES["Dougga"],
        "description": "A remarkably well-preserved Roman archaeological site listed by UNESCO. It features a theatre, temples, and a forum set in exceptional natural surroundings."
    },
    {
        "name": "Monastir Ribat",
        "city": "Monastir",
        "image": MONUMENT_IMAGES["Monastir Ribat"],
        "description": "An 8th-century Islamic military fortress with panoramic views over the sea and town. Typical Arabic military architecture with watchtowers and ramparts."
    },
    {
        "name": "Tunis Medina",
        "city": "Tunis",
        "image": MONUMENT_IMAGES["Tunis Medina"],
        "description": "Historic centre of Tunis and a UNESCO World Heritage site. Labyrinthine alleys, lively souks, and preserved Arab-Andalusian architecture."
    },
    {
        "name": "Sousse Medina",
        "city": "Sousse",
        "image": MONUMENT_IMAGES["Sousse Medina"],
        "description": "A fortified medina listed by UNESCO. Impressive ramparts, a historic ribat, and 9th-century military architecture."
    },
    {
        "name": "Sfax Medina",
        "city": "Sfax",
        "image": MONUMENT_IMAGES["Sfax Medina"],
        "description": "The largest medina in North Africa, with preserved traditional architecture and authentic market districts specialized by trade."
    },
    {
        "name": "Bourguiba Mausoleum",
        "city": "Monastir",
        "image": MONUMENT_IMAGES["Bourguiba Mausoleum"],
        "description": "The tomb of the father of Tunisian independence, featuring modern architecture inspired by Islamic art with golden domes and white marble."
    },
    {
        "name": "Saint-Louis Cathedral",
        "city": "Carthage",
        "image": MONUMENT_IMAGES["Saint-Louis Cathedral"],
        "description": "A former Catholic cathedral in a Byzantine style with sweeping views over the Gulf of Tunis; a reminder of the French colonial era."
    },
    {
        "name": "Kelibia Fort",
        "city": "Kelibia",
        "image": MONUMENT_IMAGES["Kelibia Fort"],
        "description": "A fortress of Byzantine and later Arabic origin with panoramic views over the sea and Cape Bon peninsula. Mediterranean military architecture at its best."
    },
    {
        "name": "Kef Citadel",
        "city": "Le Kef",
        "image": MONUMENT_IMAGES["Kef Citadel"],
        "description": "An Ottoman citadel perched on a rock offering sweeping views of the Atlas Mountains and the historic town of Kef."
    },
    {
        "name": "Zitouna Mosque",
        "city": "Tunis",
        "image": MONUMENT_IMAGES["Zitouna Mosque"],
        "description": "The main mosque of Tunis with Arab-Andalusian architecture, a center of Islamic learning since the 8th century."
    },
    {
        "name": "Bizerte Port",
        "city": "Bizerte",
        "image": MONUMENT_IMAGES["Bizerte Port"],
        "description": "A historic port with fortifications that reflect Tunisia's maritime past and military architecture."
    },
    {
        "name": "Bulla Regia Site",
        "city": "Jendouba",
        "image": MONUMENT_IMAGES["Bulla Regia Site"],
        "description": "A unique Roman site known for its underground houses designed to keep interiors cool in the hot climate."
    },
    {
        "name": "Thuburbo Majus Site",
        "city": "Zaghouan",
        "image": MONUMENT_IMAGES["Thuburbo Majus Site"],
        "description": "A Roman town with a forum, temples and baths; classical Roman architecture well preserved in a rural setting."
    },
    {
        "name": "Testour Medina",
        "city": "Testour",
        "image": MONUMENT_IMAGES["Testour Medina"],
        "description": "An Andalusian-influenced medina with unique architecture and culinary traditions inherited from Moriscos."
    },
    {
        "name": "Makthar Site",
        "city": "Makthar",
        "image": MONUMENT_IMAGES["Makthar Site"],
        "description": "An archaeological site with Numidian and Roman remains, including a well-preserved triumphal arch and forum."
    }
]

# Instantiate AI agent early so sidebar controls always work
ai = AIAgent()

# Dynamic filters
cities = [all_cities_label] + sorted(list({m["city"] for m in MONUMENTS}))
selected_city = st.selectbox(city_label, cities)

# Filtering
filtered = [m for m in MONUMENTS if selected_city == all_cities_label or m["city"] == selected_city]

if not filtered:
    st.warning(no_mon_text)
else:
    # Responsive grid display
    cols_per_row = get_responsive_columns()
    try:
        cols_per_row = max(1, int(cols_per_row))
    except Exception:
        cols_per_row = 1

    cols = st.columns(cols_per_row)

    for i, mon in enumerate(filtered):
        with cols[i % cols_per_row]:
            with st.container():
                image_path = os.path.join("images", mon["image"]) if mon.get("image") else None
                if image_path and os.path.exists(image_path):
                    responsive_image_display(image_path, mon["name"])
                else:
                    st.error(f"{img_not_found_text}: {mon.get('image')}")

                st.subheader(mon["name"])
                st.markdown(f"**{city_label} :** {mon['city']}")
                st.write(mon["description"])

                # Favorites button
                item = {
                    "id": mon["name"],
                    "name": mon["name"],
                    "description": mon["description"],
                    "location": mon["city"],
                    "type": "monument"
                }
                add_to_favorites_button("monuments", item, f"fav_{mon['name']}")

                # AI explanation button
                if st.button(f"🧠 {ai_explain_label} {mon['name']}", key=f"explain_{mon['name']}"):
                    with st.spinner(ai_explain_loading):
                        prompt = (
                            f"Explain the detailed history, cultural and architectural significance of the following Tunisian monument: {mon['name']}. "
                            "Include historical periods, architectural influences and interesting anecdotes. Keep it to 5-6 sentences."
                        )
                        explanation = ai.ask(prompt)
                        st.success(explanation)

                st.markdown("---")

# Sidebar statistics
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 {stats_label}**")
st.sidebar.markdown(f"**{total_label} :** {len(MONUMENTS)} {monuments_label}")
st.sidebar.markdown(f"**{shown_label} :** {len(filtered)} {monuments_label}")

# Sidebar AI recommendation
if st.sidebar.button(f"🎯 {must_see_label}"):
    with st.sidebar.spinner(ai_recommend_loading):
        names_list = ", ".join([m['name'] for m in MONUMENTS])
        prompt = (
            f"Among these Tunisian monuments: {names_list}, which is the most impressive and why? "
            "Give a personalized recommendation in 3-4 sentences."
        )
        recommendation = ai.ask(prompt)
        st.sidebar.success(recommendation)
