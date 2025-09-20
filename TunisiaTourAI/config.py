"""
Configuration for TunisiaTourAI
Performance optimizations and parameters management (English version)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Application configuration
APP_CONFIG = {
    "name": "TunisiaTourAI",
    "version": "2.0.0",
    "description": "Intelligent guide for Tunisia",
    "author": "TunisiaTourAI Team",
    "language": "en",
    "theme": "tunisian"
}

# Tunisian color palette
TUNISIAN_COLORS = {
    "primary": "#E70013",      # Tunisian red
    "primary_dark": "#B3000F", # Dark red
    "white": "#FFFFFF",
    "light": "#F8F9FA",
    "gray": "#6C757D",
    "dark": "#1E1E1E",
    "gold": "#FFD700"
}

# AI configuration
AI_CONFIG = {
    "model": "models/gemini-2.0-flash-exp",
    "max_tokens": 1000,
    "temperature": 0.7,
    "context_window": 8000,
    "timeout": 30
}

# Image configuration
IMAGE_CONFIG = {
    "max_size": 5 * 1024 * 1024,  # 5MB
    "allowed_formats": [".jpg", ".jpeg", ".png", ".webp"],
    "thumbnail_size": (800, 600),
    "quality": 85
}

# Performance configuration
PERFORMANCE_CONFIG = {
    "cache_ttl": 3600,  # 1 hour
    "max_concurrent_requests": 5,
    "request_timeout": 30,
    "enable_caching": True,
    "enable_compression": True
}

# Data configuration
DATA_CONFIG = {
    "destinations_file": "data/destinations.json",
    "monuments_file": "data/monuments.json",
    "festivals_file": "data/festivals.json",
    "images_folder": "images/",
    "backup_folder": "backups/"
}

# Security configuration
SECURITY_CONFIG = {
    "max_file_upload_size": 10 * 1024 * 1024,  # 10MB
    "allowed_file_types": ["jpg", "jpeg", "png", "webp"],
    "enable_rate_limiting": True,
    "max_requests_per_minute": 60
}

# Error messages (English)
ERROR_MESSAGES = {
    "api_key_missing": "Gemini API key missing. Please configure GEMINI_API_KEY in your .env or Streamlit secrets.",
    "quota_exceeded": "Usage limit exceeded. Please wait a few minutes.",
    "image_not_found": "Image not found in the images/ folder",
    "invalid_request": "Invalid request. Please check your parameters.",
    "timeout": "Request timed out. Please try again.",
    "network_error": "Network error. Please check your internet connection."
}

# Tunisian regions configuration (English)
TUNISIAN_REGIONS = {
    "North": {
        "name": "North",
        "cities": ["Tunis", "Bizerte", "Nabeul", "Hammamet", "Sidi Bou Saïd", "Tabarka", "Aïn Draham"],
        "description": "Coastal region with beaches and mountains"
    },
    "Center": {
        "name": "Center",
        "cities": ["Sousse", "Monastir", "Mahdia", "Sfax", "Kairouan", "Le Kef"],
        "description": "Historical and cultural region"
    },
    "South": {
        "name": "South",
        "cities": ["Tozeur", "Djerba", "Zarzis", "Gafsa", "Tataouine"],
        "description": "Desert region and oases"
    }
}

# Travel types (English keys and content)
TRAVEL_TYPES = {
    "cultural": {
        "name": "Cultural",
        "description": "Focus on history and monuments",
        "destinations": ["Carthage", "Dougga", "El Jem", "Kairouan"]
    },
    "beach": {
        "name": "Beach",
        "description": "Beaches and water activities",
        "destinations": ["Hammamet", "Sousse", "Djerba", "Tabarka"]
    },
    "adventure": {
        "name": "Adventure",
        "description": "Desert and outdoor activities",
        "destinations": ["Tozeur", "Tataouine", "Gafsa"]
    },
    "gastronomic": {
        "name": "Gastronomic",
        "description": "Culinary discovery",
        "destinations": ["Tunis", "Sfax", "Testour"]
    }
}

# Seasons configuration (English)
SEASONS = {
    "spring": {
        "name": "Spring",
        "months": [3, 4, 5],
        "description": "Mild temperatures, ideal for sightseeing",
        "festivals": ["Medina Festival", "Nabeul Festival"]
    },
    "summer": {
        "name": "Summer",
        "months": [6, 7, 8],
        "description": "Hot and dry, many festivals",
        "festivals": ["Carthage International Festival", "Tabarka Jazz Festival"]
    },
    "autumn": {
        "name": "Autumn",
        "months": [9, 10, 11],
        "description": "Pleasant temperatures, fewer tourists",
        "festivals": ["Testour Festival", "Sfax Festival"]
    },
    "winter": {
        "name": "Winter",
        "months": [12, 1, 2],
        "description": "Mild on the coast, colder in the mountains",
        "festivals": ["Tozeur Festival"]
    }
}

# Budget levels (English)
BUDGET_LEVELS = {
    "budget": {
        "name": "Budget",
        "daily_budget": 50,
        "description": "Simple accommodation, local meals",
        "accommodation": "Hostels, 2-3 star hotels",
        "transport": "Buses, trains, economical car rental"
    },
    "mid": {
        "name": "Mid",
        "daily_budget": 100,
        "description": "Comfortable accommodation, varied restaurants",
        "accommodation": "3-4 star hotels",
        "transport": "Car rental, taxis"
    },
    "high": {
        "name": "High",
        "daily_budget": 200,
        "description": "Luxury accommodation, fine dining",
        "accommodation": "4-5 star hotels, riads",
        "transport": "Premium car rental, chauffeur"
    },
    "luxury": {
        "name": "Luxury",
        "daily_budget": 500,
        "description": "Full premium experience",
        "accommodation": "Luxury hotels, private villas",
        "transport": "Private driver, VIP transfers"
    }
}


def get_config(section, key=None):
    """Retrieve a configuration section or a specific key"""
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
        raise ValueError(f"Configuration section '{section}' not found")

    if key:
        return configs[section].get(key)
    return configs[section]


def get_api_key():
    """Get the Gemini API key from the environment"""
    return os.getenv('GEMINI_API_KEY')


def is_development():
    """Return True if running in development mode"""
    return os.getenv('ENVIRONMENT', 'production') == 'development'


def get_cache_ttl():
    """Get cache TTL (seconds)"""
    return PERFORMANCE_CONFIG.get('cache_ttl', 3600)
