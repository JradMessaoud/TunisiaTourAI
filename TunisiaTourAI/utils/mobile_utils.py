import streamlit as st
import re

def is_mobile_device():
    """
    Détecte si l'utilisateur est sur un appareil mobile
    Basé sur le User-Agent et la taille d'écran
    """
    # Récupérer le User-Agent depuis les paramètres de session
    user_agent = st.get_option("server.headless")
    
    # Patterns pour détecter les appareils mobiles
    mobile_patterns = [
        r'Android',
        r'iPhone',
        r'iPad',
        r'Mobile',
        r'BlackBerry',
        r'Windows Phone'
    ]
    
    # Vérifier si c'est un appareil mobile
    is_mobile = any(re.search(pattern, str(user_agent), re.IGNORECASE) 
                   for pattern in mobile_patterns)
    
    return is_mobile

def get_responsive_columns():
    """
    Retourne le nombre de colonnes approprié selon la taille d'écran
    """
    if is_mobile_device():
        return 1
    else:
        return 2

def get_mobile_layout():
    """
    Retourne les paramètres de layout pour mobile
    """
    return {
        'columns': 1,
        'image_height': 200,
        'card_padding': '1rem',
        'button_width': '100%',
        'font_size': '0.9rem'
    }

def get_desktop_layout():
    """
    Retourne les paramètres de layout pour desktop
    """
    return {
        'columns': 2,
        'image_height': 300,
        'card_padding': '1.5rem',
        'button_width': 'auto',
        'font_size': '1rem'
    }

def get_current_layout():
    """
    Retourne le layout approprié selon l'appareil
    """
    if is_mobile_device():
        return get_mobile_layout()
    else:
        return get_desktop_layout()

def create_responsive_grid(items, items_per_row=None):
    """
    Crée une grille responsive pour afficher des éléments
    """
    layout = get_current_layout()
    columns = items_per_row or layout['columns']
    
    # Sur mobile, forcer une colonne
    if is_mobile_device():
        columns = 1
    
    # Créer les colonnes
    cols = st.columns(columns)
    
    return cols

def responsive_image_display(image_path, caption="", use_container_width=True):
    """
    Affiche une image de manière responsive
    """
    layout = get_current_layout()
    
    try:
        st.image(
            image_path,
            caption=caption,
            use_container_width=use_container_width,
            output_format="PNG"
        )
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {e}")

def responsive_button(text, key=None, **kwargs):
    """
    Crée un bouton responsive avec les bonnes dimensions
    """
    layout = get_current_layout()
    
    # Ajouter les styles CSS pour le bouton responsive
    st.markdown(f"""
    <style>
    .responsive-button-{key if key else 'default'} {{
        width: {layout['button_width']} !important;
        height: 44px !important;
        font-size: {layout['font_size']} !important;
        margin: 5px 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    return st.button(text, key=key, **kwargs)

def responsive_card(container, title="", content="", image_path=None):
    """
    Crée une carte responsive
    """
    layout = get_current_layout()
    
    with container:
        st.markdown(f"""
        <div class="responsive-card" style="
            padding: {layout['card_padding']};
            margin: 10px 0;
            border-radius: 12px;
            background: rgba(255,255,255,0.08);
            border: 1.5px solid rgba(231,0,19,0.18);
        ">
        """, unsafe_allow_html=True)
        
        if image_path:
            responsive_image_display(image_path)
        
        if title:
            st.subheader(title)
        
        if content:
            st.write(content)
        
        st.markdown("</div>", unsafe_allow_html=True)

def add_mobile_navigation():
    """
    Ajoute une navigation mobile optimisée
    """
    if is_mobile_device():
        st.markdown("""
        <style>
        .mobile-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(26,26,26,0.95);
            backdrop-filter: blur(10px);
            border-top: 2px solid #E70013;
            z-index: 1000;
            padding: 10px;
        }
        
        .mobile-nav-item {
            display: inline-block;
            margin: 0 10px;
            text-align: center;
            color: #fff;
            text-decoration: none;
            font-size: 0.8rem;
        }
        
        .mobile-nav-item:hover {
            color: #E70013;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="mobile-nav">
            <a href="/" class="mobile-nav-item">🏠</a>
            <a href="/1_🏖️_Destinations" class="mobile-nav-item">🏖️</a>
            <a href="/2_🗿_Monuments" class="mobile-nav-item">🗿</a>
            <a href="/3_🎉_Événements" class="mobile-nav-item">🎉</a>
            <a href="/4_🤖_ChatAvecIA" class="mobile-nav-item">🤖</a>
            <a href="/5_🗺️_Planificateur" class="mobile-nav-item">🗺️</a>
            <a href="/6_❤️_Favoris" class="mobile-nav-item">❤️</a>
        </div>
        """, unsafe_allow_html=True)

def optimize_for_mobile():
    """
    Applique les optimisations générales pour mobile
    """
    if is_mobile_device():
        # Réduire la taille des images
        st.markdown("""
        <style>
        .stImage > img {
            max-height: 200px !important;
            object-fit: cover !important;
        }
        
        .stButton > button {
            width: 100% !important;
            height: 44px !important;
            font-size: 16px !important;
        }
        
        .stSelectbox > div {
            width: 100% !important;
        }
        
        .stTextInput > div {
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True) 