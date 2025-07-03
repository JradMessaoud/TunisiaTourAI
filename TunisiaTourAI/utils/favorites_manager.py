"""
Gestionnaire de favoris pour TunisiaTourAI
Permet aux utilisateurs de sauvegarder leurs lieux préférés
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

class FavoritesManager:
    def __init__(self, favorites_file: str = "favorites.json"):
        """
        Initialise le gestionnaire de favoris
        
        Args:
            favorites_file: Fichier de stockage des favoris
        """
        self.favorites_file = favorites_file
        self.favorites = self._load_favorites()
    
    def _load_favorites(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Charge les favoris depuis le fichier
        
        Returns:
            Dictionnaire des favoris par catégorie
        """
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Structure par défaut
        return {
            "destinations": [],
            "monuments": [],
            "festivals": [],
            "itineraries": []
        }
    
    def _save_favorites(self) -> bool:
        """
        Sauvegarde les favoris dans le fichier
        
        Returns:
            True si succès, False sinon
        """
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def add_favorite(self, category: str, item: Dict[str, Any]) -> bool:
        """
        Ajoute un élément aux favoris
        
        Args:
            category: Catégorie (destinations, monuments, festivals, itineraries)
            item: Élément à ajouter
            
        Returns:
            True si ajouté, False sinon
        """
        if category not in self.favorites:
            return False
        
        # Vérifier si l'élément existe déjà
        item_id = item.get('id') or item.get('name')
        existing_items = [f for f in self.favorites[category] 
                         if (f.get('id') == item_id or f.get('name') == item_id)]
        
        if existing_items:
            return False  # Déjà dans les favoris
        
        # Ajouter la date d'ajout
        item['added_date'] = datetime.now().isoformat()
        item['favorite_id'] = f"{category}_{len(self.favorites[category]) + 1}"
        
        self.favorites[category].append(item)
        return self._save_favorites()
    
    def remove_favorite(self, category: str, item_id: str) -> bool:
        """
        Supprime un élément des favoris
        
        Args:
            category: Catégorie
            item_id: ID de l'élément à supprimer
            
        Returns:
            True si supprimé, False sinon
        """
        if category not in self.favorites:
            return False
        
        # Trouver et supprimer l'élément
        self.favorites[category] = [
            item for item in self.favorites[category]
            if item.get('favorite_id') != item_id and item.get('id') != item_id and item.get('name') != item_id
        ]
        
        return self._save_favorites()
    
    def get_favorites(self, category: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Récupère les favoris
        
        Args:
            category: Catégorie spécifique ou None pour toutes
            
        Returns:
            Dictionnaire des favoris
        """
        if category:
            return {category: self.favorites.get(category, [])}
        return self.favorites
    
    def is_favorite(self, category: str, item_id: str) -> bool:
        """
        Vérifie si un élément est dans les favoris
        
        Args:
            category: Catégorie
            item_id: ID de l'élément
            
        Returns:
            True si favori, False sinon
        """
        if category not in self.favorites:
            return False
        
        return any(
            item.get('favorite_id') == item_id or 
            item.get('id') == item_id or 
            item.get('name') == item_id
            for item in self.favorites[category]
        )
    
    def get_favorites_count(self, category: Optional[str] = None) -> int:
        """
        Compte le nombre de favoris
        
        Args:
            category: Catégorie spécifique ou None pour toutes
            
        Returns:
            Nombre de favoris
        """
        if category:
            return len(self.favorites.get(category, []))
        
        return sum(len(items) for items in self.favorites.values())
    
    def clear_favorites(self, category: Optional[str] = None) -> bool:
        """
        Vide les favoris
        
        Args:
            category: Catégorie spécifique ou None pour toutes
            
        Returns:
            True si vidé, False sinon
        """
        if category:
            if category in self.favorites:
                self.favorites[category] = []
        else:
            self.favorites = {
                "destinations": [],
                "monuments": [],
                "festivals": [],
                "itineraries": []
            }
        
        return self._save_favorites()

# Instance globale du gestionnaire de favoris
favorites_manager = FavoritesManager()

def get_favorites_manager():
    """
    Obtient l'instance du gestionnaire de favoris
    
    Returns:
        Instance de FavoritesManager
    """
    return favorites_manager

# Fonctions utilitaires pour Streamlit
def add_to_favorites_button(category: str, item: Dict[str, Any], key: str = None):
    """
    Affiche un bouton pour ajouter/retirer des favoris
    
    Args:
        category: Catégorie de l'élément
        item: Élément à ajouter/retirer
        key: Clé unique pour Streamlit
    """
    item_id = item.get('id') or item.get('name')
    is_fav = favorites_manager.is_favorite(category, item_id)
    
    if key is None:
        key = f"fav_{category}_{item_id}"
    
    if is_fav:
        if st.button("❤️ Retirer des favoris", key=key):
            if favorites_manager.remove_favorite(category, item_id):
                st.success("Retiré des favoris !")
                st.rerun()
            else:
                st.error("Erreur lors de la suppression")
    else:
        if st.button("🤍 Ajouter aux favoris", key=key):
            if favorites_manager.add_favorite(category, item):
                st.success("Ajouté aux favoris !")
                st.rerun()
            else:
                st.error("Erreur lors de l'ajout")

def display_favorites_page():
    """
    Affiche la page des favoris
    """
    st.title("❤️ Mes Favoris")
    
    # Statistiques
    total_favorites = favorites_manager.get_favorites_count()
    if total_favorites == 0:
        st.info("Vous n'avez pas encore de favoris. Explorez l'application et ajoutez vos lieux préférés !")
        return
    
    # Onglets par catégorie
    categories = ["destinations", "monuments", "festivals", "itineraries"]
    tab_names = ["🏖️ Destinations", "🗿 Monuments", "🎉 Festivals", "🗺️ Itinéraires"]
    
    tabs = st.tabs(tab_names)
    
    for i, (tab, category) in enumerate(zip(tabs, categories)):
        with tab:
            favorites = favorites_manager.get_favorites(category)
            items = favorites.get(category, [])
            
            if not items:
                st.info(f"Aucun favori dans la catégorie {category}")
                continue
            
            # Affichage des favoris
            for item in items:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {item.get('name', 'Sans nom')}")
                        if item.get('description'):
                            st.write(item['description'])
                        if item.get('location'):
                            st.write(f"📍 {item['location']}")
                        if item.get('added_date'):
                            added_date = datetime.fromisoformat(item['added_date']).strftime("%d/%m/%Y")
                            st.write(f"📅 Ajouté le {added_date}")
                    
                    with col2:
                        if st.button("🗑️ Supprimer", key=f"del_{category}_{item.get('favorite_id')}"):
                            if favorites_manager.remove_favorite(category, item.get('favorite_id')):
                                st.success("Supprimé !")
                                st.rerun()
                            else:
                                st.error("Erreur")
                    
                    st.divider()
    
    # Bouton pour tout supprimer
    if st.button("🗑️ Supprimer tous les favoris", type="secondary"):
        if favorites_manager.clear_favorites():
            st.success("Tous les favoris ont été supprimés !")
            st.rerun()
        else:
            st.error("Erreur lors de la suppression") 