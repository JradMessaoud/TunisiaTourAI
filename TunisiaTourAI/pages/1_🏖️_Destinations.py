import streamlit as st
import os
from agents.ai_agent import AIAgent
from utils.favorites_manager import add_to_favorites_button
from utils.translate import translate_text

st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

st.title(TEXTS.get('dest_title', {}).get(lang, '🏖️ Destinations populaires en Tunisie'))

# Mapping des destinations vers les images locales
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

# Données complètes de destinations
DESTINATIONS = [
    {
        "nom": "Sidi Bou Saïd",
        "region": "Nord",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Sidi Bou Saïd"],
        "description": "Un village pittoresque aux maisons blanches et volets bleus, perché sur une falaise surplombant la Méditerranée. Célèbre pour ses cafés traditionnels et ses vues panoramiques."
    },
    {
        "nom": "Tozeur",
        "region": "Sud",
        "type": "Désert",
        "image": DESTINATION_IMAGES["Tozeur"],
        "description": "Porte du désert, célèbre pour ses oasis, ses palmeraies et son architecture en briques d'argile. Découvrez les traditions berbères et les paysages sahariens."
    },
    {
        "nom": "Hammamet",
        "region": "Nord",
        "type": "Plage",
        "image": DESTINATION_IMAGES["Hammamet"],
        "description": "Station balnéaire réputée pour ses plages de sable fin et sa médina animée. Parfait pour les vacances en famille et les activités nautiques."
    },
    {
        "nom": "Aïn Draham",
        "region": "Nord",
        "type": "Montagne",
        "image": DESTINATION_IMAGES["Aïn Draham"],
        "description": "Village de montagne entouré de forêts, idéal pour la randonnée et l'écotourisme. Climat frais et paysages verdoyants toute l'année."
    },
    {
        "nom": "Djerba",
        "region": "Sud",
        "type": "Île",
        "image": DESTINATION_IMAGES["Djerba"],
        "description": "La plus grande île de Tunisie, célèbre pour ses plages paradisiaques, sa culture juive unique et ses traditions artisanales."
    },
    {
        "nom": "Tabarka",
        "region": "Nord",
        "type": "Plage",
        "image": DESTINATION_IMAGES["Tabarka"],
        "description": "Station balnéaire côtière avec des plages sauvages, des falaises impressionnantes et une forêt de pins. Idéale pour la plongée."
    },
    {
        "nom": "Monastir",
        "region": "Centre",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Monastir"],
        "description": "Ville côtière historique avec un ribat impressionnant, des plages tranquilles et un aéroport international. Berceau de l'ancien président Bourguiba."
    },
    {
        "nom": "Sousse",
        "region": "Centre",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Sousse"],
        "description": "Troisième ville de Tunisie, célèbre pour sa médina classée UNESCO, ses plages animées et son port de plaisance moderne."
    },
    {
        "nom": "Nabeul",
        "region": "Nord",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Nabeul"],
        "description": "Capitale de la poterie tunisienne, réputée pour son artisanat traditionnel, ses marchés colorés et ses plages familiales."
    },
    {
        "nom": "Kelibia",
        "region": "Nord",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Kelibia"],
        "description": "Petite ville côtière avec une forteresse historique, des plages sauvages et une ambiance authentique et préservée."
    },
    {
        "nom": "Zarzis",
        "region": "Sud",
        "type": "Plage",
        "image": DESTINATION_IMAGES["Zarzis"],
        "description": "Station balnéaire du sud avec des plages de sable blanc, des palmiers et une ambiance décontractée typique du sud tunisien."
    },
    {
        "nom": "Gafsa",
        "region": "Centre",
        "type": "Oasis",
        "image": DESTINATION_IMAGES["Gafsa"],
        "description": "Ville oasis historique avec des sources thermales naturelles, une palmeraie verdoyante et un riche patrimoine archéologique."
    },
    {
        "nom": "Le Kef",
        "region": "Nord-Ouest",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Le Kef"],
        "description": "Ville de montagne avec une citadelle byzantine impressionnante, des ruines romaines et un climat frais en été."
    },
    {
        "nom": "Bizerte",
        "region": "Nord",
        "type": "Port",
        "image": DESTINATION_IMAGES["Bizerte"],
        "description": "Plus ancienne ville de Tunisie, célèbre pour son port de pêche traditionnel, ses plages sauvages et son lac salé unique."
    },
    {
        "nom": "Mahdia",
        "region": "Centre",
        "type": "Ville",
        "image": DESTINATION_IMAGES["Mahdia"],
        "description": "Ancienne capitale fatimide avec une péninsule historique, des plages tranquilles et un port de pêche authentique."
    }
]

regions = [TEXTS.get('all_regions', {}).get(lang, 'Toutes')] + sorted(list(set(d["region"] for d in DESTINATIONS)))
types = [TEXTS.get('all_types', {}).get(lang, 'Tous')] + sorted(list(set(d["type"] for d in DESTINATIONS)))
region = st.selectbox(TEXTS.get('region_label', {}).get(lang, 'Région'), regions)
type_lieu = st.selectbox(TEXTS.get('type_label', {}).get(lang, 'Type'), types)

filtered = [d for d in DESTINATIONS if (region == TEXTS.get('all_regions', {}).get(lang, 'Toutes') or d["region"] == region) and (type_lieu == TEXTS.get('all_types', {}).get(lang, 'Tous') or d["type"] == type_lieu)]

if not filtered:
    st.warning(TEXTS.get('no_dest', {}).get(lang, 'Aucune destination trouvée pour ces critères.'))
else:
    ai = AIAgent()
    for dest in filtered:
        with st.container():
            cols = st.columns([1,2])
            with cols[0]:
                image_path = os.path.join("images", dest["image"])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.error(TEXTS.get('img_not_found', {}).get(lang, f"Image non trouvée: {dest['image']}"))
            with cols[1]:
                st.subheader(dest["nom"])
                st.markdown(f"**{{TEXTS.get('region_label', {{}}).get(lang, 'Région')}} :** {dest['region']}  ")
                st.markdown(f"**{{TEXTS.get('type_label', {{}}).get(lang, 'Type')}} :** {dest['type']}  ")
                st.write(dest["description"])
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🧠 {{TEXTS.get('ai_opinion', {{}}).get(lang, 'Avis IA sur')}} {dest['nom']}", key=f"ai_{dest['nom']}"):
                        with st.spinner(TEXTS.get('ai_opinion_loading', {{}}).get(lang, 'Génération de l\'avis IA...')):
                            avis = ai.ask(f"Donne-moi un avis de voyageur sur la destination tunisienne suivante : {dest['nom']}. Fais-le en 3 phrases maximum.")
                            st.success(avis)
                with col2:
                    item = {
                        "id": dest["nom"],
                        "name": dest["nom"],
                        "description": dest["description"],
                        "location": dest["region"],
                        "type": dest["type"]
                    }
                    add_to_favorites_button("destinations", item, f"fav_{dest['nom']}")
            st.markdown("---")

st.info(TEXTS.get('dest_dynamic', {{}}).get(lang, 'Affichage dynamique des destinations à venir…'))

if st.button(TEXTS.get('ai_summary', {{}}).get(lang, 'Générer un résumé IA sur les destinations')):
    ai = AIAgent()
    st.write(ai.ask("Donne-moi un résumé des meilleures destinations touristiques en Tunisie.")) 