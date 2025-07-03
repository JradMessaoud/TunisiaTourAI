import streamlit as st
import os
from agents.ai_agent import AIAgent
from utils.translate import translate_text
from utils.favorites_manager import add_to_favorites_button

st.session_state["lang"] = "fr"
lang = "fr"
TEXTS = st.session_state.get('TEXTS', {})

st.title("🎉 Événements et festivals traditionnels")

# Mapping des festivals vers les VRAIES images de festivals
FESTIVAL_IMAGES = {
    "Festival International de Carthage": "festivzl de Carthage.jpg",
    "Festival des Ksour": "festival de ksour.jpg",
    "Festival de la Médina": "festival l medina tunis.jpg",
    "Festival de Jazz de Tabarka": "festival de tabarka.jpeg",
    "Festival de Sousse": "festival sousse.png",
    "Festival de Hammamet": "festival hammamet.jpg",
    "Festival de Djerba": "festival ulysse djerba.jpg",
    "Festival de Testour": "festival testour.jpg",
    "Festival de Tozeur": "festival-oasis-tozeur.jpg",
    "Festival de Kairouan": "festival de kairaoun.jpg",
    "Festival de Monastir": "Festival de Monastir.jpg",
    "Festival de Nabeul": "festival-de nabeul.jpg",
    "Festival de Bizerte": "Festival-de-Bizerte.-049.jpg",
    "Festival de Mahdia": "nuits de mahdia festival.jpg",
    "Festival de Sfax": "festival sfax.jpg",
    "Festival de Gafsa": "festival de gafsa.jpg",
    "Festival de Le Kef": "sicca jazz el kef.png",
    "Festival de Zarzis": "festival des sponges zarzis.jpg",
    "Festival de Aïn Draham": "cinemontagnes ain drahem.jpg"
}

# Données enrichies d'événements
EVENEMENTS = [
    {
        "nom": "Festival International de Carthage",
        "type": "Festival",
        "ville": "Carthage",
        "image": FESTIVAL_IMAGES["Festival International de Carthage"],
        "description": "Festival de musique et arts du spectacle dans l'amphithéâtre de Carthage. Artistes internationaux et locaux dans un cadre historique unique.",
        "periode": "Juillet-Août"
    },
    {
        "nom": "Festival des Ksour",
        "type": "Festival",
        "ville": "Tataouine",
        "image": FESTIVAL_IMAGES["Festival des Ksour"],
        "description": "Festival culturel dans les villages berbères du sud. Traditions, musique et artisanat local dans les ksour traditionnels.",
        "periode": "Mars"
    },
    {
        "nom": "Festival de la Médina",
        "type": "Festival",
        "ville": "Tunis",
        "image": FESTIVAL_IMAGES["Festival de la Médina"],
        "description": "Festival des arts traditionnels dans la médina de Tunis. Musique, danse et artisanat dans les ruelles historiques.",
        "periode": "Avril"
    },
    {
        "nom": "Festival de Jazz de Tabarka",
        "type": "Musique",
        "ville": "Tabarka",
        "image": FESTIVAL_IMAGES["Festival de Jazz de Tabarka"],
        "description": "Festival de jazz international dans un cadre idyllique. Musiciens du monde entier dans un environnement naturel exceptionnel.",
        "periode": "Juillet"
    },
    {
        "nom": "Festival de Sousse",
        "type": "Festival",
        "ville": "Sousse",
        "image": FESTIVAL_IMAGES["Festival de Sousse"],
        "description": "Festival des arts et de la culture dans la médina de Sousse. Spectacles et expositions dans un cadre historique préservé.",
        "periode": "Août"
    },
    {
        "nom": "Festival de Hammamet",
        "type": "Festival",
        "ville": "Hammamet",
        "image": FESTIVAL_IMAGES["Festival de Hammamet"],
        "description": "Festival international de théâtre et arts du spectacle. Performances dans le théâtre en plein air avec vue sur la mer.",
        "periode": "Juillet"
    },
    {
        "nom": "Festival de Djerba",
        "type": "Festival",
        "ville": "Djerba",
        "image": FESTIVAL_IMAGES["Festival de Djerba"],
        "description": "Festival des traditions insulaires. Musique, danse et gastronomie locale dans l'île aux mille couleurs.",
        "periode": "Juin"
    },
    {
        "nom": "Festival de Testour",
        "type": "Gastronomie",
        "ville": "Testour",
        "image": FESTIVAL_IMAGES["Festival de Testour"],
        "description": "Festival de la gastronomie andalouse. Traditions culinaires espagnoles en Tunisie avec influences morisques.",
        "periode": "Septembre"
    },
    {
        "nom": "Festival de Tozeur",
        "type": "Festival",
        "ville": "Tozeur",
        "image": FESTIVAL_IMAGES["Festival de Tozeur"],
        "description": "Festival des oasis et du désert. Traditions sahariennes et artisanat local dans la porte du Sahara.",
        "periode": "Décembre"
    },
    {
        "nom": "Festival de Kairouan",
        "type": "Religieux",
        "ville": "Kairouan",
        "image": FESTIVAL_IMAGES["Festival de Kairouan"],
        "description": "Festival religieux et culturel. Cérémonies spirituelles et musique sacrée dans la ville sainte de l'Islam.",
        "periode": "Avril"
    },
    {
        "nom": "Festival de Monastir",
        "type": "Festival",
        "ville": "Monastir",
        "image": FESTIVAL_IMAGES["Festival de Monastir"],
        "description": "Festival des arts et de la culture. Spectacles dans le ribat historique avec vue panoramique sur la mer.",
        "periode": "Août"
    },
    {
        "nom": "Festival de Nabeul",
        "type": "Artisanat",
        "ville": "Nabeul",
        "image": FESTIVAL_IMAGES["Festival de Nabeul"],
        "description": "Festival de la poterie et de l'artisanat. Démonstrations et ventes d'artisanat local dans la capitale de la poterie.",
        "periode": "Mai"
    },
    {
        "nom": "Festival de Bizerte",
        "type": "Festival",
        "ville": "Bizerte",
        "image": FESTIVAL_IMAGES["Festival de Bizerte"],
        "description": "Festival maritime et culturel. Traditions portuaires et spectacles nautiques dans la plus ancienne ville de Tunisie.",
        "periode": "Juillet"
    },
    {
        "nom": "Festival de Mahdia",
        "type": "Festival",
        "ville": "Mahdia",
        "image": FESTIVAL_IMAGES["Festival de Mahdia"],
        "description": "Festival des arts et de la culture. Spectacles dans la médina fortifiée sur la péninsule historique.",
        "periode": "Août"
    },
    {
        "nom": "Festival de Sfax",
        "type": "Festival",
        "ville": "Sfax",
        "image": FESTIVAL_IMAGES["Festival de Sfax"],
        "description": "Festival international de la médina. Arts traditionnels et modernes dans la plus grande médina d'Afrique du Nord.",
        "periode": "Septembre"
    },
    {
        "nom": "Festival de Gafsa",
        "type": "Festival",
        "ville": "Gafsa",
        "image": FESTIVAL_IMAGES["Festival de Gafsa"],
        "description": "Festival des oasis et de la culture saharienne. Traditions du sud tunisien dans l'oasis historique.",
        "periode": "Novembre"
    },
    {
        "nom": "Festival de Le Kef",
        "type": "Festival",
        "ville": "Le Kef",
        "image": FESTIVAL_IMAGES["Festival de Le Kef"],
        "description": "Festival de montagne et de culture berbère. Traditions montagnardes et musique locale dans la citadelle historique.",
        "periode": "Juin"
    },
    {
        "nom": "Festival de Zarzis",
        "type": "Festival",
        "ville": "Zarzis",
        "image": FESTIVAL_IMAGES["Festival de Zarzis"],
        "description": "Festival du sud et des traditions sahariennes. Musique et artisanat local dans la station balnéaire du sud.",
        "periode": "Octobre"
    },
    {
        "nom": "Festival de Aïn Draham",
        "type": "Festival",
        "ville": "Aïn Draham",
        "image": FESTIVAL_IMAGES["Festival de Aïn Draham"],
        "description": "Festival de montagne et d'écotourisme. Randonnées et traditions montagnardes dans les forêts du nord.",
        "periode": "Mai"
    }
]

# Filtres dynamiques
types = ["Tous"] + sorted(list(set(e["type"] for e in EVENEMENTS)))
villes = ["Toutes"] + sorted(list(set(e["ville"] for e in EVENEMENTS)))
type_event = st.selectbox("Type d'événement", types)
ville = st.selectbox("Ville", villes)

# Filtrage
filtered = [e for e in EVENEMENTS if (type_event == "Tous" or e["type"] == type_event) and (ville == "Toutes" or e["ville"] == ville)]

if not filtered:
    st.warning("Aucun événement trouvé pour ces critères.")
else:
    ai = AIAgent()
    
    # Affichage en grille
    cols = st.columns(2)
    for i, event in enumerate(filtered):
        with cols[i % 2]:
            with st.container():
                # Utiliser l'image locale
                image_path = os.path.join("images", event["image"])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True, caption=event["nom"])
                else:
                    st.error(f"Image non trouvée: {event['image']}")
                
                st.subheader(event["nom"])
                st.markdown(f"**Type :** {event['type']}  ")
                st.markdown(f"**Ville :** {event['ville']}  ")
                st.markdown(f"**Période :** {event['periode']}  ")
                st.write(event["description"])
                # Ajout du bouton favoris
                item = {
                    "id": event["nom"],
                    "name": event["nom"],
                    "description": event["description"],
                    "location": event["ville"],
                    "type": event["type"]
                }
                add_to_favorites_button("festivals", item, f"fav_{event['nom']}")
                
                # Bouton pour description IA
                if st.button(f"🧠 Description IA sur {event['nom']}", key=f"description_{event['nom']}"):
                    with st.spinner("Génération de la description IA..."):
                        description = ai.ask(f"Décris-moi en détail l'événement tunisien suivant : {event['nom']}. Inclus l'histoire, l'importance culturelle, les activités proposées et l'ambiance. Fais-le en 5-6 phrases maximum.")
                        st.success(description)
                
                st.markdown("---")

# Statistiques
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Statistiques**")
st.sidebar.markdown(f"**Total :** {len(EVENEMENTS)} événements")
st.sidebar.markdown(f"**Affichés :** {len(filtered)} événements")

# Recommandation IA
if st.sidebar.button("🎯 Festival à ne pas manquer"):
    with st.spinner("Génération de recommandation..."):
        recommendation = ai.ask("Quel est le festival ou événement culturel le plus important et incontournable en Tunisie ? Donne-moi une recommandation avec les raisons de sa visite. Fais-le en 3 phrases maximum.")
        st.sidebar.success(recommendation) 