import streamlit as st
import os
from agents.ai_agent import AIAgent
from utils.translate import translate_text
from utils.favorites_manager import add_to_favorites_button

st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

st.title(TEXTS.get('mon_title', {}).get(lang, '🗿 Monuments historiques de Tunisie'))

# Mapping des monuments vers les images locales
MONUMENT_IMAGES = {
    "Colisée d'El Jem": "Amphi_El_Jem.jpg",
    "Mosquée Okba": "800px-Grande_Mosquée_de_Kairouan,_vue_d'ensemble.jpg",
    "Site de Carthage": "Carthage.JPG",
    "Dougga": "Dougga.jpg",
    "Ribat de Monastir": "MONASTIR_RIBAT.jpg",
    "Médina de Tunis": "medina_tunis.jpg",
    "Médina de Sousse": "MEDINA OF SOUSSE.jpg",
    "Médina de Sfax": "MEDINA OF _Sfax.jpg",
    "Mausolée de Bourguiba": "bourguiba_mausoleum.jpg",
    "Cathédrale Saint-Louis": "CATHEDRAL SAINT LOUIS CARTHAGE.jpg",
    "Fort de Kélibia": "Fort_de_kelibia_3.jpg",
    "Citadelle du Kef": "KEF CITADELLE.jpg",
    "Mosquée Zitouna": "zitouna.jpg",
    "Port de Bizerte": "port_de_BIZERTE-Tunisie.jpg",
    "Site de Bulla Regia": "bulla_regia.jpg",
    "Site de Thuburbo Majus": "thuburbo_majus.jpg",
    "Médina de Testour": "Testour.jpg",
    "Site de Makthar": "MAKTHAR.jpg"
}

# Données enrichies de monuments
MONUMENTS = [
    {
        "nom": "Colisée d'El Jem",
        "ville": "El Jem",
        "image": MONUMENT_IMAGES["Colisée d'El Jem"],
        "description": "Un amphithéâtre romain impressionnant, classé au patrimoine mondial de l'UNESCO. Troisième plus grand amphithéâtre du monde romain après Rome et Capoue."
    },
    {
        "nom": "Mosquée Okba",
        "ville": "Kairouan",
        "image": MONUMENT_IMAGES["Mosquée Okba"],
        "description": "L'une des plus anciennes et prestigieuses mosquées du monde musulman. Centre spirituel de l'Islam en Afrique du Nord et quatrième lieu saint de l'Islam."
    },
    {
        "nom": "Site de Carthage",
        "ville": "Carthage",
        "image": MONUMENT_IMAGES["Site de Carthage"],
        "description": "Ruines antiques d'une cité mythique, centre de la civilisation carthaginoise. Classé au patrimoine mondial de l'UNESCO, témoin de l'histoire punique et romaine."
    },
    {
        "nom": "Dougga",
        "ville": "Téboursouk",
        "image": MONUMENT_IMAGES["Dougga"],
        "description": "Un site archéologique romain remarquablement préservé, inscrit à l'UNESCO. Théâtre, temples et forum parfaitement conservés dans un cadre naturel exceptionnel."
    },
    {
        "nom": "Ribat de Monastir",
        "ville": "Monastir",
        "image": MONUMENT_IMAGES["Ribat de Monastir"],
        "description": "Forteresse militaire islamique du 8ème siècle. Vue panoramique sur la mer et la ville. Architecture militaire arabe typique avec tours de guet et remparts."
    },
    {
        "nom": "Médina de Tunis",
        "ville": "Tunis",
        "image": MONUMENT_IMAGES["Médina de Tunis"],
        "description": "Centre historique de Tunis, classé UNESCO. Ruelles labyrinthiques, souks animés et architecture traditionnelle arabo-andalouse préservée."
    },
    {
        "nom": "Médina de Sousse",
        "ville": "Sousse",
        "image": MONUMENT_IMAGES["Médina de Sousse"],
        "description": "Médina fortifiée classée UNESCO. Remparts impressionnants, ribat historique et architecture militaire arabe du 9ème siècle."
    },
    {
        "nom": "Médina de Sfax",
        "ville": "Sfax",
        "image": MONUMENT_IMAGES["Médina de Sfax"],
        "description": "Plus grande médina d'Afrique du Nord. Architecture traditionnelle préservée et ambiance authentique avec ses souks spécialisés."
    },
    {
        "nom": "Mausolée de Bourguiba",
        "ville": "Monastir",
        "image": MONUMENT_IMAGES["Mausolée de Bourguiba"],
        "description": "Tombeau du père de l'indépendance tunisienne. Architecture moderne inspirée de l'art islamique avec dômes dorés et marbre blanc."
    },
    {
        "nom": "Cathédrale Saint-Louis",
        "ville": "Carthage",
        "image": MONUMENT_IMAGES["Cathédrale Saint-Louis"],
        "description": "Ancienne cathédrale catholique de style byzantin. Vue imprenable sur le golfe de Tunis et témoin de l'époque coloniale française."
    },
    {
        "nom": "Fort de Kélibia",
        "ville": "Kélibia",
        "image": MONUMENT_IMAGES["Fort de Kélibia"],
        "description": "Forteresse byzantine puis arabe. Vue panoramique sur la mer et la péninsule du Cap Bon. Architecture militaire méditerranéenne."
    },
    {
        "nom": "Citadelle du Kef",
        "ville": "Le Kef",
        "image": MONUMENT_IMAGES["Citadelle du Kef"],
        "description": "Citadelle ottomane perchée sur un rocher. Vue imprenable sur les montagnes de l'Atlas et la ville historique du Kef."
    },
    {
        "nom": "Mosquée Zitouna",
        "ville": "Tunis",
        "image": MONUMENT_IMAGES["Mosquée Zitouna"],
        "description": "Plus grande mosquée de Tunis. Architecture arabo-andalouse et centre d'enseignement islamique depuis le 8ème siècle."
    },
    {
        "nom": "Port de Bizerte",
        "ville": "Bizerte",
        "image": MONUMENT_IMAGES["Port de Bizerte"],
        "description": "Port historique avec ses fortifications. Mélange d'architecture militaire et portuaire, témoin de l'histoire maritime tunisienne."
    },
    {
        "nom": "Site de Bulla Regia",
        "ville": "Jendouba",
        "image": MONUMENT_IMAGES["Site de Bulla Regia"],
        "description": "Site romain unique avec des maisons souterraines. Architecture adaptée au climat chaud avec des pièces enterrées pour la fraîcheur."
    },
    {
        "nom": "Site de Thuburbo Majus",
        "ville": "Zaghouan",
        "image": MONUMENT_IMAGES["Site de Thuburbo Majus"],
        "description": "Cité romaine avec forum, temples et thermes. Architecture romaine classique bien préservée dans un cadre rural."
    },
    {
        "nom": "Médina de Testour",
        "ville": "Testour",
        "image": MONUMENT_IMAGES["Médina de Testour"],
        "description": "Médina andalouse avec architecture unique. Influence espagnole et traditions culinaires héritées des Morisques."
    },
    {
        "nom": "Site de Makthar",
        "ville": "Makthar",
        "image": MONUMENT_IMAGES["Site de Makthar"],
        "description": "Site archéologique avec vestiges numides et romains. Arc de triomphe et forum bien conservés dans un paysage de steppe."
    }
]

# Filtres dynamiques
villes = [TEXTS.get('all_cities', {}).get(lang, 'Toutes')] + sorted(list(set(m["ville"] for m in MONUMENTS)))
ville = st.selectbox(TEXTS.get('city_label', {}).get(lang, 'Ville/Région'), villes)

# Filtrage
filtered = [m for m in MONUMENTS if ville == TEXTS.get('all_cities', {}).get(lang, 'Toutes') or m["ville"] == ville]

if not filtered:
    st.warning(TEXTS.get('no_mon', {}).get(lang, 'Aucun monument trouvé pour cette ville/région.'))
else:
    ai = AIAgent()
    
    # Affichage en grille
    cols = st.columns(2)
    for i, mon in enumerate(filtered):
        with cols[i % 2]:
            with st.container():
                # Utiliser l'image locale
                image_path = os.path.join("images", mon["image"])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True, caption=mon["nom"])
                else:
                    st.error(TEXTS.get('img_not_found', {}).get(lang, f"Image non trouvée: {mon['image']}"))
                
                st.subheader(mon["nom"])
                st.markdown(f"**{TEXTS.get('city_label', {}).get(lang, 'Ville')} :** {mon['ville']}")
                st.write(mon["description"])
                # Ajout du bouton favoris
                item = {
                    "id": mon["nom"],
                    "name": mon["nom"],
                    "description": mon["description"],
                    "location": mon["ville"],
                    "type": "monument"
                }
                add_to_favorites_button("monuments", item, f"fav_{mon['nom']}")
                
                # Bouton pour explication IA
                if st.button(f"🧠 {TEXTS.get('ai_explain', {}).get(lang, 'Explication IA sur')} {mon['nom']}", key=f"explication_{mon['nom']}"):
                    with st.spinner(TEXTS.get('ai_explain_loading', {}).get(lang, 'Génération de l\'explication IA...')):
                        explication = ai.ask(f"Explique-moi l'histoire détaillée, l'importance culturelle et architecturale du monument suivant en Tunisie : {mon['nom']}. Inclus les périodes historiques, les influences architecturales et les anecdotes intéressantes. Fais-le en 5-6 phrases maximum.")
                        st.success(explication)
                
                st.markdown("---")

# Statistiques
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 {TEXTS.get('stats', {}).get(lang, 'Statistiques')}**")
st.sidebar.markdown(f"**{TEXTS.get('total', {}).get(lang, 'Total')} :** {len(MONUMENTS)} {TEXTS.get('monuments', {}).get(lang, 'monuments')}")
st.sidebar.markdown(f"**{TEXTS.get('shown', {}).get(lang, 'Affichés')} :** {len(filtered)} {TEXTS.get('monuments', {}).get(lang, 'monuments')}")

# Recommandation IA
if st.sidebar.button(f"🎯 {TEXTS.get('must_see', {}).get(lang, 'Monument à ne pas manquer')}"):
    with st.spinner(TEXTS.get('ai_recommend_loading', {}).get(lang, 'Génération de recommandation...')):
        recommendation = ai.ask("Quel est le monument historique le plus impressionnant et incontournable à visiter en Tunisie ? Donne-moi une recommandation avec les raisons de sa visite. Fais-le en 3 phrases maximum.")
        st.sidebar.success(recommendation) 