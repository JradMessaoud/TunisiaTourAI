import streamlit as st
import os
from agents.ai_agent import AIAgent
from utils.favorites_manager import add_to_favorites_button
from utils.translate import translate_text
from utils.mobile_utils import get_responsive_columns, responsive_image_display, optimize_for_mobile

# Mobile optimizations
optimize_for_mobile()

st.session_state["lang"] = "en"
lang = "en"
TEXTS = st.session_state.get('TEXTS', {})

st.title(TEXTS.get('dest_title', {}).get(lang, '🏖️ Popular Destinations in Tunisia'))

# Mapping destinations to local images
DESTINATION_IMAGES = {
    "Sidi Bou Saïd": "1024px-Sidi_Bou_Said,_Tunisia,_19_March_2018_DSC_8004.jpg",
    "Tozeur": "Tozeur_Avenue_Habib_Bourguiba.JPG",
    "Hammamet": "HAMMAMET.jpg",
    "Aïn Draham": "1024px-Ain_Draham_s_brouillard.jpeg",
    "Djerba": "djerba.jpg",
    "Tabarka": "TABARKA.jpeg",
    "Monastir": "View_of_Monastir_from_the_ribat_tower.jpg",
    "Sousse": "Sousse_Marina.jpg",
    "Nabeul": "Ville_de_Nabeul,_13_avril_2023,_20230413_160128.jpg",
    "Kelibia": "KELIBIA.jpg",
    "Zarzis": "ZARZIS.jpg",
    "Gafsa": "Gafsa.jpg",
    "Le Kef": "KEF CITADELLE.jpg",
    "Bizerte": "BIZERTE.JPG",
    "Mahdia": "Mahdia.jpg"
}

# Complete destinations data
DESTINATIONS = [
    {
        "name": "Sidi Bou Saïd",
        "region": "North",
        "type": "City",
        "image": DESTINATION_IMAGES["Sidi Bou Saïd"],
        "description": "A picturesque village with white houses and blue shutters, perched on a cliff overlooking the Mediterranean. Famous for its traditional cafés and panoramic views."
    },
    {
        "name": "Tozeur",
        "region": "South",
        "type": "Desert",
        "image": DESTINATION_IMAGES["Tozeur"],
        "description": "Gateway to the desert, known for its oases, palm groves, and clay brick architecture. Discover Berber traditions and Saharan landscapes."
    },
    {
        "name": "Hammamet",
        "region": "North",
        "type": "Beach",
        "image": DESTINATION_IMAGES["Hammamet"],
        "description": "Renowned seaside resort with fine sandy beaches and a lively medina. Perfect for family vacations and water sports."
    },
    {
        "name": "Aïn Draham",
        "region": "North",
        "type": "Mountain",
        "image": DESTINATION_IMAGES["Aïn Draham"],
        "description": "Mountain village surrounded by forests, ideal for hiking and ecotourism. Cool climate and green landscapes all year round."
    },
    {
        "name": "Djerba",
        "region": "South",
        "type": "Island",
        "image": DESTINATION_IMAGES["Djerba"],
        "description": "The largest island in Tunisia, famous for its paradise beaches, unique Jewish culture, and traditional crafts."
    },
    {
        "name": "Tabarka",
        "region": "North",
        "type": "Beach",
        "image": DESTINATION_IMAGES["Tabarka"],
        "description": "Coastal resort with wild beaches, stunning cliffs, and a pine forest. Ideal for scuba diving."
    },
    {
        "name": "Monastir",
        "region": "Center",
        "type": "City",
        "image": DESTINATION_IMAGES["Monastir"],
        "description": "Historic coastal city with an impressive ribat, peaceful beaches, and an international airport. Birthplace of former President Bourguiba."
    },
    {
        "name": "Sousse",
        "region": "Center",
        "type": "City",
        "image": DESTINATION_IMAGES["Sousse"],
        "description": "Tunisia’s third-largest city, famous for its UNESCO-listed medina, lively beaches, and modern marina."
    },
    {
        "name": "Nabeul",
        "region": "North",
        "type": "City",
        "image": DESTINATION_IMAGES["Nabeul"],
        "description": "Capital of Tunisian pottery, known for traditional crafts, colorful markets, and family-friendly beaches."
    },
    {
        "name": "Kelibia",
        "region": "North",
        "type": "City",
        "image": DESTINATION_IMAGES["Kelibia"],
        "description": "Small coastal town with a historic fortress, unspoiled beaches, and an authentic preserved atmosphere."
    },
    {
        "name": "Zarzis",
        "region": "South",
        "type": "Beach",
        "image": DESTINATION_IMAGES["Zarzis"],
        "description": "Southern seaside resort with white sandy beaches, palm trees, and a laid-back vibe typical of southern Tunisia."
    },
    {
        "name": "Gafsa",
        "region": "Center",
        "type": "Oasis",
        "image": DESTINATION_IMAGES["Gafsa"],
        "description": "Historic oasis town with natural hot springs, a lush palm grove, and rich archaeological heritage."
    },
    {
        "name": "Le Kef",
        "region": "North-West",
        "type": "City",
        "image": DESTINATION_IMAGES["Le Kef"],
        "description": "Mountain town with an impressive Byzantine citadel, Roman ruins, and a refreshing summer climate."
    },
    {
        "name": "Bizerte",
        "region": "North",
        "type": "Port",
        "image": DESTINATION_IMAGES["Bizerte"],
        "description": "Tunisia’s oldest city, famous for its traditional fishing port, wild beaches, and unique salt lake."
    },
    {
        "name": "Mahdia",
        "region": "Center",
        "type": "City",
        "image": DESTINATION_IMAGES["Mahdia"],
        "description": "Former Fatimid capital with a historic peninsula, peaceful beaches, and an authentic fishing port."
    }
]

# ✅ FIXED PART
regions = [TEXTS.get('all_regions', {}).get(lang, 'All')] + sorted(list(set(d["region"] for d in DESTINATIONS)))
types = [TEXTS.get('all_types', {}).get(lang, 'All')] + sorted(list(set(d["type"] for d in DESTINATIONS)))
region = st.selectbox(TEXTS.get('region_label', {}).get(lang, 'Region'), regions)
place_type = st.selectbox(TEXTS.get('type_label', {}).get(lang, 'Type'), types)

filtered = [
    d for d in DESTINATIONS
    if (region == TEXTS.get('all_regions', {}).get(lang, 'All') or d["region"] == region)
    and (place_type == TEXTS.get('all_types', {}).get(lang, 'All') or d["type"] == place_type)
]

if not filtered:
    st.warning(TEXTS.get('no_dest', {}).get(lang, 'No destinations found for these criteria.'))
else:
    ai = AIAgent()
    
    # Responsive layout for destinations
    cols_per_row = get_responsive_columns()
    
    for dest in filtered:
        with st.container():
            # On mobile, show single column
            if cols_per_row == 1:
                # Image on top
                image_path = os.path.join("images", dest["image"])
                if os.path.exists(image_path):
                    responsive_image_display(image_path, dest["name"])
                else:
                    st.error(TEXTS.get('img_not_found', {}).get(lang, f"Image not found: {dest['image']}"))
                
                # Content below
                st.subheader(dest["name"])
                st.markdown(f"**{TEXTS.get('region_label', {}).get(lang, 'Region')} :** {dest['region']}")
                st.markdown(f"**{TEXTS.get('type_label', {}).get(lang, 'Type')} :** {dest['type']}")
                st.write(dest["description"])
                
                # Buttons in columns on mobile
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🧠 {TEXTS.get('ai_opinion', {}).get(lang, 'AI Opinion on')} {dest['name']}", key=f"ai_{dest['name']}"):
                        with st.spinner(TEXTS.get('ai_opinion_loading', {}).get(lang, 'Generating AI opinion...')):
                            opinion = ai.ask(f"Give me a traveler’s opinion on the following Tunisian destination: {dest['name']}. Keep it within 3 sentences.")
                            st.success(opinion)
                with col2:
                    item = {
                        "id": dest["name"],
                        "name": dest["name"],
                        "description": dest["description"],
                        "location": dest["region"],
                        "type": dest["type"]
                    }
                    add_to_favorites_button("destinations", item, f"fav_{dest['name']}")
            
            else:
                # Desktop layout: image left, content right
                cols = st.columns([1, 2])
                with cols[0]:
                    image_path = os.path.join("images", dest["image"])
                    if os.path.exists(image_path):
                        responsive_image_display(image_path, dest["name"])
                    else:
                        st.error(TEXTS.get('img_not_found', {}).get(lang, f"Image not found: {dest['image']}"))
                with cols[1]:
                    st.subheader(dest["name"])
                    st.markdown(f"**{TEXTS.get('region_label', {}).get(lang, 'Region')} :** {dest['region']}")
                    st.markdown(f"**{TEXTS.get('type_label', {}).get(lang, 'Type')} :** {dest['type']}")
                    st.write(dest["description"])
                    
                    # Buttons side by side on desktop
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🧠 {TEXTS.get('ai_opinion', {}).get(lang, 'AI Opinion on')} {dest['name']}", key=f"ai_{dest['name']}"):
                            with st.spinner(TEXTS.get('ai_opinion_loading', {}).get(lang, 'Generating AI opinion...')):
                                opinion = ai.ask(f"Give me a traveler’s opinion on the following Tunisian destination: {dest['name']}. Keep it within 3 sentences.")
                                st.success(opinion)
                    with col2:
                        item = {
                            "id": dest["name"],
                            "name": dest["name"],
                            "description": dest["description"],
                            "location": dest["region"],
                            "type": dest["type"]
                        }
                        add_to_favorites_button("destinations", item, f"fav_{dest['name']}")
            
            st.markdown("---")

st.info(TEXTS.get('dest_dynamic', {}).get(lang, 'Dynamic display of more destinations coming soon…'))

if st.button(TEXTS.get('ai_summary', {}).get(lang, 'Generate AI Summary of Destinations')):
    ai = AIAgent()
    st.write(ai.ask("Give me a summary of the best tourist destinations in Tunisia."))
