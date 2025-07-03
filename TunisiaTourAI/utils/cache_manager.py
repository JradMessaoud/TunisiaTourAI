"""
Gestionnaire de cache pour TunisiaTourAI
Optimise les performances en mettant en cache les réponses IA
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import pickle

class CacheManager:
    def __init__(self, cache_dir: str = "cache", ttl_hours: int = 24):
        """
        Initialise le gestionnaire de cache
        
        Args:
            cache_dir: Répertoire de stockage du cache
            ttl_hours: Durée de vie du cache en heures
        """
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        
        # Créer le répertoire de cache s'il n'existe pas
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _generate_key(self, data: str) -> str:
        """
        Génère une clé de cache basée sur le contenu
        
        Args:
            data: Données à hasher
            
        Returns:
            Clé de cache unique
        """
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """
        Obtient le chemin du fichier de cache
        
        Args:
            key: Clé de cache
            
        Returns:
            Chemin du fichier de cache
        """
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def _is_expired(self, cache_path: str) -> bool:
        """
        Vérifie si le cache a expiré
        
        Args:
            cache_path: Chemin du fichier de cache
            
        Returns:
            True si expiré, False sinon
        """
        if not os.path.exists(cache_path):
            return True
        
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        expiry_time = file_time + timedelta(hours=self.ttl_hours)
        
        return datetime.now() > expiry_time
    
    def get(self, key_data: str) -> Optional[Any]:
        """
        Récupère une valeur du cache
        
        Args:
            key_data: Données pour générer la clé
            
        Returns:
            Valeur mise en cache ou None si non trouvée/expirée
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        
        if self._is_expired(cache_path):
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.PickleError):
            return None
    
    def set(self, key_data: str, value: Any) -> bool:
        """
        Stocke une valeur dans le cache
        
        Args:
            key_data: Données pour générer la clé
            value: Valeur à stocker
            
        Returns:
            True si succès, False sinon
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            return True
        except Exception:
            return False
    
    def delete(self, key_data: str) -> bool:
        """
        Supprime une entrée du cache
        
        Args:
            key_data: Données pour générer la clé
            
        Returns:
            True si supprimé, False sinon
        """
        key = self._generate_key(key_data)
        cache_path = self._get_cache_path(key)
        
        try:
            if os.path.exists(cache_path):
                os.remove(cache_path)
            return True
        except Exception:
            return False
    
    def clear(self) -> bool:
        """
        Vide tout le cache
        
        Returns:
            True si succès, False sinon
        """
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.pkl'):
                    os.remove(os.path.join(self.cache_dir, filename))
            return True
        except Exception:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtient les statistiques du cache
        
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')]
            total_size = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in files)
            
            expired_count = 0
            for filename in files:
                cache_path = os.path.join(self.cache_dir, filename)
                if self._is_expired(cache_path):
                    expired_count += 1
            
            return {
                "total_entries": len(files),
                "expired_entries": expired_count,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_dir": self.cache_dir,
                "ttl_hours": self.ttl_hours
            }
        except Exception:
            return {"error": "Impossible de récupérer les statistiques"}
    
    def cleanup_expired(self) -> int:
        """
        Nettoie les entrées expirées du cache
        
        Returns:
            Nombre d'entrées supprimées
        """
        deleted_count = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.pkl'):
                    cache_path = os.path.join(self.cache_dir, filename)
                    if self._is_expired(cache_path):
                        os.remove(cache_path)
                        deleted_count += 1
        except Exception:
            pass
        
        return deleted_count

# Instance globale du cache
cache_manager = CacheManager()

def cached_response(func):
    """
    Décorateur pour mettre en cache les réponses de fonctions
    
    Args:
        func: Fonction à décorer
        
    Returns:
        Fonction décorée avec cache
    """
    def wrapper(*args, **kwargs):
        # Créer une clé unique basée sur les arguments
        key_data = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
        
        # Vérifier le cache
        cached_result = cache_manager.get(key_data)
        if cached_result is not None:
            return cached_result
        
        # Exécuter la fonction
        result = func(*args, **kwargs)
        
        # Mettre en cache le résultat
        cache_manager.set(key_data, result)
        
        return result
    
    return wrapper 