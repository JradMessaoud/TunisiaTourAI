# 🇹🇳 TunisiaTourAI

**Votre guide intelligent pour découvrir la beauté et la richesse de la Tunisie**

Une application Streamlit moderne qui combine l'intelligence artificielle avec une base de données complète sur les destinations, monuments et festivals tunisiens.

## ✨ Fonctionnalités Principales

### 🏖️ Destinations
- **15 destinations** couvrant tout le territoire tunisien
- Images authentiques de Wikimedia Commons
- Filtres par région et type de destination
- Avis IA personnalisés pour chaque lieu
- Système de favoris intégré

### 🗿 Monuments
- **18 monuments** historiques et culturels
- Sites archéologiques et religieux
- Descriptions détaillées avec contexte historique
- Recommandations IA pour la visite

### 🎉 Festivals
- **19 festivals** et événements culturels
- Calendrier saisonnier complet
- Informations pratiques et culturelles
- Festivals traditionnels et modernes

### 🤖 Assistant IA Tunisien
- **Gemini 2.0 Flash** pour des réponses intelligentes
- Spécialisé uniquement sur la Tunisie
- Réponses en français détaillées et engageantes
- Cache intelligent pour optimiser les performances

### 🗺️ Planificateur de Voyage
- Interface interactive pour créer des itinéraires
- Paramètres personnalisables (durée, budget, intérêts)
- Génération d'itinéraires par l'IA
- Exemples d'itinéraires populaires

### ❤️ Système de Favoris
- Sauvegarde des lieux préférés
- Organisation par catégorie
- Interface dédiée pour gérer les favoris
- Persistance des données

## 🚀 Nouvelles Fonctionnalités (v2.0)

### ⚡ Optimisations Performance
- **Système de cache** pour les réponses IA
- Réduction des appels API répétés
- Chargement optimisé des images
- Interface responsive

### 📊 Monitoring et Logs
- **Système de logs** complet
- Monitoring des performances
- Suivi des requêtes IA
- Statistiques d'utilisation

### 🎨 Interface Améliorée
- **Design tunisien** (rouge et blanc)
- Animations et transitions
- Interface moderne et intuitive
- Thème cohérent sur toutes les pages

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Clé API Gemini (Google AI Studio)

### Installation
```bash
# Cloner le repository
git clone <repository-url>
cd TunisiaTourAI

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'API
# Créer un fichier .env avec votre clé Gemini
echo "GEMINI_API_KEY=votre_cle_api" > .env

# Lancer l'application
streamlit run TunisiaTourAI/app.py
```

## 📁 Structure du Projet

```
TunisiaTourAI/
├── TunisiaTourAI/
│   ├── app.py                 # Application principale
│   ├── config.py              # Configuration globale
│   ├── agents/
│   │   └── ai_agent.py        # Agent IA avec cache et logs
│   ├── pages/
│   │   ├── 1_🏖️_Destinations.py
│   │   ├── 2_🗿_Monuments.py
│   │   ├── 3_🎉_Événements.py
│   │   ├── 4_🤖_ChatAvecIA.py
│   │   ├── 5_🗺️_Planificateur.py  # Nouveau !
│   │   └── 6_❤️_Favoris.py        # Nouveau !
│   └── utils/
│       ├── cache_manager.py   # Gestionnaire de cache
│       ├── favorites_manager.py # Gestionnaire de favoris
│       └── logger.py          # Système de logs
├── images/                    # Images locales
├── cache/                     # Cache des réponses IA
├── logs/                      # Fichiers de logs
├── favorites.json             # Favoris utilisateur
└── requirements.txt
```

## 🎯 Utilisation

### Navigation
1. **Page d'accueil** : Vue d'ensemble et assistant IA rapide
2. **Destinations** : Explorez les lieux par région et type
3. **Monuments** : Découvrez l'histoire tunisienne
4. **Festivals** : Participez aux événements culturels
5. **Planificateur** : Créez votre itinéraire personnalisé
6. **Favoris** : Gérez vos lieux préférés
7. **Chat IA** : Posez vos questions sur la Tunisie

### Fonctionnalités Avancées
- **Favoris** : Cliquez sur 🤍 pour ajouter aux favoris
- **Cache IA** : Les réponses sont mises en cache automatiquement
- **Logs** : Monitoring automatique des performances
- **Responsive** : Interface adaptée mobile et desktop

## 🔧 Configuration

### Variables d'Environnement
```env
GEMINI_API_KEY=votre_cle_api_gemini
```

### Configuration Avancée
Modifiez `config.py` pour personnaliser :
- Couleurs du thème
- Paramètres de cache
- Configuration IA
- Régions et types de voyage

## 📊 Statistiques

- **15 destinations** couvrant 3 régions
- **18 monuments** historiques
- **19 festivals** saisonniers
- **32 images** authentiques
- **Cache IA** pour optimiser les performances
- **Système de logs** pour le monitoring

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📝 TODO

- [ ] Intégration de cartes interactives
- [ ] Système de notation et avis
- [ ] Mode sombre
- [ ] Support multilingue complet
- [ ] Export d'itinéraires en PDF
- [ ] Intégration météo en temps réel
- [ ] Système de notifications

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Développeur

**Jrad Messaoud** - Développé avec ❤️ pour la Tunisie

---

*TunisiaTourAI - Votre guide intelligent pour découvrir la Tunisie* 🇹🇳 