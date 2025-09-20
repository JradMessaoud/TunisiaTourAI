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
title_text = TEXTS.get('fest_title', {}).get(lang, '🎉 Traditional Events & Festivals')
type_label = TEXTS.get('type_label', {}).get(lang, 'Type')
city_label = TEXTS.get('city_label', {}).get(lang, 'City')
all_label = TEXTS.get('all_label', {}).get(lang, 'All')
img_not_found_text = TEXTS.get('img_not_found', {}).get(lang, 'Image not found')
no_event_text = TEXTS.get('no_event', {}).get(lang, 'No events found for these criteria.')
ai_desc_label = TEXTS.get('ai_desc', {}).get(lang, 'AI description for')
ai_desc_loading = TEXTS.get('ai_desc_loading', {}).get(lang, 'Generating AI description...')
stats_label = TEXTS.get('stats', {}).get(lang, 'Statistics')
total_label = TEXTS.get('total', {}).get(lang, 'Total')
shown_label = TEXTS.get('shown', {}).get(lang, 'Shown')
events_label = TEXTS.get('events', {}).get(lang, 'events')
recommend_label = TEXTS.get('recommend_label', {}).get(lang, 'Festival not to miss')
ai_recommend_loading = TEXTS.get('ai_recommend_loading', {}).get(lang, 'Generating recommendation...')

st.title(title_text)

# Mapping festivals to local image filenames
FESTIVAL_IMAGES = {
    "Carthage International Festival": "festivzl de Carthage.jpg",
    "Ksour Festival": "festival de ksour.jpg",
    "Medina Festival": "festival l medina tunis.jpg",
    "Tabarka Jazz Festival": "festival de tabarka.jpeg",
    "Sousse Festival": "festival sousse.png",
    "Hammamet Festival": "festival hammamet.jpg",
    "Djerba Festival": "festival ulysse djerba.jpg",
    "Testour Festival": "festival testour.jpg",
    "Tozeur Festival": "festival-oasis-tozeur.jpg",
    "Kairouan Festival": "festival de kairaoun.jpg",
    "Monastir Festival": "Festival de Monastir.jpg",
    "Nabeul Festival": "festival-de nabeul.jpg",
    "Bizerte Festival": "Festival-de-Bizerte.-049.jpg",
    "Mahdia Festival": "nuits de mahdia festival.jpg",
    "Sfax Festival": "festival sfax.jpg",
    "Gafsa Festival": "festival de gafsa.jpg",
    "Le Kef Festival": "sicca jazz el kef.png",
    "Zarzis Festival": "festival des sponges zarzis.jpg",
    "Ain Draham Festival": "cinemontagnes ain drahem.jpg"
}

# Festivals data (English keys and descriptions)
FESTIVALS = [
    {
        "name": "Carthage International Festival",
        "type": "Festival",
        "city": "Carthage",
        "image": FESTIVAL_IMAGES["Carthage International Festival"],
        "description": "Music and performing arts festival held in the Roman amphitheatre of Carthage. Features international and local artists in a unique historic setting.",
        "period": "July-August"
    },
    {
        "name": "Ksour Festival",
        "type": "Festival",
        "city": "Tataouine",
        "image": FESTIVAL_IMAGES["Ksour Festival"],
        "description": "Cultural festival in the Berber villages of the south celebrating traditions, music and local crafts among historic ksour.",
        "period": "March"
    },
    {
        "name": "Medina Festival",
        "type": "Festival",
        "city": "Tunis",
        "image": FESTIVAL_IMAGES["Medina Festival"],
        "description": "Arts festival in the old medina of Tunis showcasing traditional music, dance and crafts in historic lanes.",
        "period": "April"
    },
    {
        "name": "Tabarka Jazz Festival",
        "type": "Music",
        "city": "Tabarka",
        "image": FESTIVAL_IMAGES["Tabarka Jazz Festival"],
        "description": "International jazz festival set in a stunning natural landscape, attracting musicians from around the world.",
        "period": "July"
    },
    {
        "name": "Sousse Festival",
        "type": "Festival",
        "city": "Sousse",
        "image": FESTIVAL_IMAGES["Sousse Festival"],
        "description": "Arts and culture festival in Sousse's medina with performances and exhibitions in a well-preserved historic setting.",
        "period": "August"
    },
    {
        "name": "Hammamet Festival",
        "type": "Festival",
        "city": "Hammamet",
        "image": FESTIVAL_IMAGES["Hammamet Festival"],
        "description": "International theatre and performing arts festival held in open-air venues with views over the sea.",
        "period": "July"
    },
    {
        "name": "Djerba Festival",
        "type": "Festival",
        "city": "Djerba",
        "image": FESTIVAL_IMAGES["Djerba Festival"],
        "description": "Island traditions festival highlighting music, dance and local gastronomy in a colorful island atmosphere.",
        "period": "June"
    },
    {
        "name": "Testour Gastronomy Festival",
        "type": "Gastronomy",
        "city": "Testour",
        "image": FESTIVAL_IMAGES["Testour Festival"],
        "description": "Festival celebrating Andalusian culinary traditions and the Morisco heritage in local cuisine.",
        "period": "September"
    },
    {
        "name": "Tozeur Oasis Festival",
        "type": "Festival",
        "city": "Tozeur",
        "image": FESTIVAL_IMAGES["Tozeur Festival"],
        "description": "Oasis and desert festival that celebrates Saharan traditions and local craftsmanship at the gateway to the Sahara.",
        "period": "December"
    },
    {
        "name": "Kairouan Religious Festival",
        "type": "Religious",
        "city": "Kairouan",
        "image": FESTIVAL_IMAGES["Kairouan Festival"],
        "description": "Religious and cultural ceremonies with spiritual music and rituals in one of Tunisia's holiest cities.",
        "period": "April"
    },
    {
        "name": "Monastir Festival",
        "type": "Festival",
        "city": "Monastir",
        "image": FESTIVAL_IMAGES["Monastir Festival"],
        "description": "Arts and culture events held within the historic ribat overlooking the sea.",
        "period": "August"
    },
    {
        "name": "Nabeul Pottery Festival",
        "type": "Crafts",
        "city": "Nabeul",
        "image": FESTIVAL_IMAGES["Nabeul Festival"],
        "description": "Festival dedicated to pottery and local crafts with demonstrations and marketplace sales in the pottery capital.",
        "period": "May"
    },
    {
        "name": "Bizerte Maritime Festival",
        "type": "Festival",
        "city": "Bizerte",
        "image": FESTIVAL_IMAGES["Bizerte Festival"],
        "description": "Maritime and cultural festival featuring port traditions and nautical performances in Tunisia's oldest city.",
        "period": "July"
    },
    {
        "name": "Mahdia Nights Festival",
        "type": "Festival",
        "city": "Mahdia",
        "image": FESTIVAL_IMAGES["Mahdia Festival"],
        "description": "Cultural nights and performances in the fortified medina on the historic peninsula.",
        "period": "August"
    },
    {
        "name": "Sfax Festival",
        "type": "Festival",
        "city": "Sfax",
        "image": FESTIVAL_IMAGES["Sfax Festival"],
        "description": "International medina festival blending traditional and contemporary arts in North Africa's largest medina.",
        "period": "September"
    },
    {
        "name": "Gafsa Oasis Festival",
        "type": "Festival",
        "city": "Gafsa",
        "image": FESTIVAL_IMAGES["Gafsa Festival"],
        "description": "Festival celebrating oasis culture and Saharan traditions in a historic oasis town.",
        "period": "November"
    },
    {
        "name": "Le Kef Mountain Festival",
        "type": "Festival",
        "city": "Le Kef",
        "image": FESTIVAL_IMAGES["Le Kef Festival"],
        "description": "Mountain and Berber culture festival featuring local music and traditions within the historic citadel.",
        "period": "June"
    },
    {
        "name": "Zarzis Southern Festival",
        "type": "Festival",
        "city": "Zarzis",
        "image": FESTIVAL_IMAGES["Zarzis Festival"],
        "description": "Southern traditions festival with music and local crafts in the southern seaside resort.",
        "period": "October"
    },
    {
        "name": "Ain Draham Mountain & Eco Festival",
        "type": "Festival",
        "city": "Ain Draham",
        "image": FESTIVAL_IMAGES["Ain Draham Festival"],
        "description": "Mountain and ecotourism festival with hiking and local mountain traditions in the northern forests.",
        "period": "May"
    }
]

# Instantiate AI agent early
ai = AIAgent()

# Dynamic filters
types = [all_label] + sorted(list({f['type'] for f in FESTIVALS}))
cities = [all_label] + sorted(list({f['city'] for f in FESTIVALS}))
selected_type = st.selectbox(type_label, types)
selected_city = st.selectbox(city_label, cities)

# Filtering
filtered = [f for f in FESTIVALS if (selected_type == all_label or f['type'] == selected_type) and (selected_city == all_label or f['city'] == selected_city)]

if not filtered:
    st.warning(no_event_text)
else:
    cols_per_row = get_responsive_columns()
    try:
        cols_per_row = max(1, int(cols_per_row))
    except Exception:
        cols_per_row = 2

    cols = st.columns(cols_per_row)

    for i, event in enumerate(filtered):
        with cols[i % cols_per_row]:
            with st.container():
                image_path = os.path.join("images", event.get('image', ''))
                if image_path and os.path.exists(image_path):
                    # use responsive display if available
                    try:
                        responsive_image_display(image_path, event['name'])
                    except Exception:
                        st.image(image_path, use_column_width=True, caption=event['name'])
                else:
                    st.error(f"{img_not_found_text}: {event.get('image')}")

                st.subheader(event['name'])
                st.markdown(f"**{type_label} :** {event['type']}  ")
                st.markdown(f"**{city_label} :** {event['city']}  ")
                st.markdown(f"**Period :** {event['period']}  ")
                st.write(event['description'])

                # Favorites button
                item = {
                    'id': event['name'],
                    'name': event['name'],
                    'description': event['description'],
                    'location': event['city'],
                    'type': event['type']
                }
                add_to_favorites_button('festivals', item, f"fav_{event['name']}")

                # AI description button
                if st.button(f"🧠 {ai_desc_label} {event['name']}", key=f"desc_{event['name']}"):
                    with st.spinner(ai_desc_loading):
                        prompt = (
                            f"Describe in detail the following Tunisian event: {event['name']}. Include its history, cultural significance, main activities, and typical atmosphere. "
                            "Keep it to 5-6 sentences."
                        )
                        description = ai.ask(prompt)
                        st.success(description)

                st.markdown("---")

# Sidebar statistics
st.sidebar.markdown('---')
st.sidebar.markdown(f"**📊 {stats_label}**")
st.sidebar.markdown(f"**{total_label} :** {len(FESTIVALS)} {events_label}")
st.sidebar.markdown(f"**{shown_label} :** {len(filtered)} {events_label}")

# Sidebar recommendation
if st.sidebar.button(f"🎯 {recommend_label}"):
    with st.sidebar.spinner(ai_recommend_loading):
        names_list = ', '.join([e['name'] for e in FESTIVALS])
        prompt = (
            f"Which of these Tunisian festivals/events is the most important and unmissable: {names_list}? "
            "Provide a short recommendation with reasons in 3 sentences."
        )
        recommendation = ai.ask(prompt)
        st.sidebar.success(recommendation)
