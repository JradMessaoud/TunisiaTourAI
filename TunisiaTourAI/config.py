"""
Configuration pour TunisiaTourAI
Optimisation des performances et gestion des paramètres
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configuration de l'application
APP_CONFIG = {
    "name": "TunisiaTourAI",
    "version": "2.0.0",
    "description": "Guide intelligent pour la Tunisie",
    "author": "TunisiaTourAI Team",
    "language": "fr",
    "theme": "tunisian"
}

# Configuration des couleurs tunisiennes
TUNISIAN_COLORS = {
    "primary": "#E70013",      # Rouge tunisien
    "primary_dark": "#B3000F", # Rouge foncé
    "white": "#FFFFFF",        # Blanc
    "light": "#F8F9FA",        # Gris clair
    "gray": "#6C757D",         # Gris
    "dark": "#1E1E1E",         # Noir
    "gold": "#FFD700"          # Or
}

# Configuration de l'IA
AI_CONFIG = {
    "model": "models/gemini-2.0-flash-exp",
    "max_tokens": 1000,
    "temperature": 0.7,
    "context_window": 8000,
    "timeout": 30
}

# Configuration des images
IMAGE_CONFIG = {
    "max_size": 5 * 1024 * 1024,  # 5MB
    "allowed_formats": [".jpg", ".jpeg", ".png", ".webp"],
    "thumbnail_size": (800, 600),
    "quality": 85
}

# Configuration des performances
PERFORMANCE_CONFIG = {
    "cache_ttl": 3600,  # 1 heure
    "max_concurrent_requests": 5,
    "request_timeout": 30,
    "enable_caching": True,
    "enable_compression": True
}

# Configuration des données
DATA_CONFIG = {
    "destinations_file": "data/destinations.json",
    "monuments_file": "data/monuments.json",
    "festivals_file": "data/festivals.json",
    "images_folder": "images/",
    "backup_folder": "backups/"
}

# Configuration de la sécurité
SECURITY_CONFIG = {
    "max_file_upload_size": 10 * 1024 * 1024,  # 10MB
    "allowed_file_types": ["jpg", "jpeg", "png", "webp"],
    "enable_rate_limiting": True,
    "max_requests_per_minute": 60
}

# Configuration des messages d'erreur
ERROR_MESSAGES = {
    "api_key_missing": "Clé API Gemini manquante. Veuillez configurer GEMINI_API_KEY dans le fichier .env",
    "quota_exceeded": "Limite d'utilisation dépassée. Veuillez attendre quelques minutes.",
    "image_not_found": "Image non trouvée dans le dossier images/",
    "invalid_request": "Requête invalide. Veuillez vérifier vos paramètres.",
    "timeout": "Délai d'attente dépassé. Veuillez réessayer.",
    "network_error": "Erreur de réseau. Vérifiez votre connexion internet."
}

# Configuration des régions tunisiennes
TUNISIAN_REGIONS = {
    "Nord": {
        "name": "Nord",
        "cities": ["Tunis", "Bizerte", "Nabeul", "Hammamet", "Sidi Bou Saïd", "Tabarka", "Aïn Draham"],
        "description": "Région côtière avec plages et montagnes"
    },
    "Centre": {
        "name": "Centre", 
        "cities": ["Sousse", "Monastir", "Mahdia", "Sfax", "Kairouan", "Le Kef"],
        "description": "Région historique et culturelle"
    },
    "Sud": {
        "name": "Sud",
        "cities": ["Tozeur", "Djerba", "Zarzis", "Gafsa", "Tataouine"],
        "description": "Région désertique et oasis"
    }
}

# Configuration des types de voyage
TRAVEL_TYPES = {
    "culturel": {
        "name": "Culturel",
        "description": "Focus sur l'histoire et les monuments",
        "destinations": ["Carthage", "Dougga", "El Jem", "Kairouan"]
    },
    "balnéaire": {
        "name": "Balnéaire", 
        "description": "Plages et activités nautiques",
        "destinations": ["Hammamet", "Sousse", "Djerba", "Tabarka"]
    },
    "aventure": {
        "name": "Aventure",
        "description": "Désert et activités outdoor",
        "destinations": ["Tozeur", "Tataouine", "Gafsa"]
    },
    "gastronomique": {
        "name": "Gastronomique",
        "description": "Découverte culinaire",
        "destinations": ["Tunis", "Sfax", "Testour"]
    }
}

# Configuration des saisons
SEASONS = {
    "printemps": {
        "name": "Printemps",
        "months": [3, 4, 5],
        "description": "Température douce, idéal pour visiter",
        "festivals": ["Festival de la Médina", "Festival de Nabeul"]
    },
    "ete": {
        "name": "Été",
        "months": [6, 7, 8],
        "description": "Chaud et sec, festivals nombreux",
        "festivals": ["Festival International de Carthage", "Festival de Jazz de Tabarka"]
    },
    "automne": {
        "name": "Automne",
        "months": [9, 10, 11],
        "description": "Température agréable, moins de touristes",
        "festivals": ["Festival de Testour", "Festival de Sfax"]
    },
    "hiver": {
        "name": "Hiver",
        "months": [12, 1, 2],
        "description": "Doux sur la côte, froid dans les montagnes",
        "festivals": ["Festival de Tozeur"]
    }
}

# Configuration des budgets
BUDGET_LEVELS = {
    "economique": {
        "name": "Économique",
        "daily_budget": 50,
        "description": "Hébergement simple, repas locaux",
        "accommodation": "Auberges, hôtels 2-3 étoiles",
        "transport": "Bus, trains, location économique"
    },
    "moyen": {
        "name": "Moyen",
        "daily_budget": 100,
        "description": "Hébergement confortable, restaurants variés",
        "accommodation": "Hôtels 3-4 étoiles",
        "transport": "Location voiture, taxis"
    },
    "eleve": {
        "name": "Élevé",
        "daily_budget": 200,
        "description": "Hébergement luxueux, restaurants gastronomiques",
        "accommodation": "Hôtels 4-5 étoiles, riads",
        "transport": "Location voiture premium, chauffeur"
    },
    "luxe": {
        "name": "Luxe",
        "daily_budget": 500,
        "description": "Expérience premium complète",
        "accommodation": "Hôtels de luxe, villas privées",
        "transport": "Chauffeur privé, transferts VIP"
    }
}

def get_config(section, key=None):
    """Récupère une configuration"""
    configs = {
        "app": APP_CONFIG,
        "colors": TUNISIAN_COLORS,
        "ai": AI_CONFIG,
        "images": IMAGE_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "data": DATA_CONFIG,
        "security": SECURITY_CONFIG,
        "errors": ERROR_MESSAGES,
        "regions": TUNISIAN_REGIONS,
        "travel_types": TRAVEL_TYPES,
        "seasons": SEASONS,
        "budgets": BUDGET_LEVELS
    }
    
    if section not in configs:
        raise ValueError(f"Section de configuration '{section}' non trouvée")
    
    if key:
        return configs[section].get(key)
    return configs[section]

def get_api_key():
    """Récupère la clé API Gemini"""
    return os.getenv('GEMINI_API_KEY')

def is_development():
    """Vérifie si l'application est en mode développement"""
    return os.getenv('ENVIRONMENT', 'production') == 'development'

def get_cache_ttl():
    """Récupère le TTL du cache"""
    return PERFORMANCE_CONFIG.get('cache_ttl', 3600) 