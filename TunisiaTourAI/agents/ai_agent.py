import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from utils.cache_manager import cached_response, cache_manager
from utils.logger import get_logger

load_dotenv()

class AIAgent:
    def __init__(self):
        """Initialise l'agent IA avec le contexte tunisien"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Clé API Gemini manquante dans le fichier .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        
        # Contexte spécifique à la Tunisie
        self.tunisian_context = """
        Vous êtes TunisiaTourAI, un expert spécialisé dans le tourisme, la culture, l'histoire et les traditions de la Tunisie.
        
        Votre rôle :
        - Répondre UNIQUEMENT aux questions concernant la Tunisie
        - Fournir des informations précises sur les destinations, monuments, festivals, culture, gastronomie, histoire, traditions
        - Donner des conseils de voyage pratiques pour la Tunisie
        - Recommander des itinéraires et activités en Tunisie
        - Expliquer les coutumes et traditions tunisiennes
        
        Si une question ne concerne pas la Tunisie, poliment redirigez vers des sujets tunisiens en disant quelque chose comme :
        "Je suis spécialisé dans la Tunisie. Puis-je vous aider avec des questions sur les destinations, monuments, festivals ou la culture tunisienne ?"
        
        Répondez toujours en français de manière détaillée, engageante et informative.
        Incluez des détails culturels, historiques et pratiques quand c'est pertinent.
        """
        
        # Initialiser le logger
        self.logger = get_logger()
    
    @cached_response
    def ask(self, question, context=None):
        """Pose une question à l'IA avec le contexte tunisien (avec cache et logs)"""
        start_time = time.time()
        
        try:
            # Combiner le contexte tunisien avec la question
            full_prompt = f"{self.tunisian_context}\n\nQuestion: {question}"
            
            if context:
                full_prompt = f"{self.tunisian_context}\n\nContexte: {context}\n\nQuestion: {question}"
            
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            
            # Logger la requête réussie
            duration = time.time() - start_time
            self.logger.log_ai_request(question, response_text, duration, True)
            
            return response_text
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Logger l'erreur
            self.logger.log_ai_request(question, str(e), duration, False)
            
            if "quota" in str(e).lower() or "429" in str(e):
                return "⚠️ Vous avez dépassé la limite gratuite de l'IA Gemini. Attendez quelques minutes ou créez une nouvelle clé API sur https://aistudio.google.com/app/apikey."
            return f"Désolé, je rencontre une difficulté technique. Veuillez réessayer. Erreur: {str(e)}"
    
    def get_tunisian_recommendation(self, category, preferences=None):
        """Obtient des recommandations spécifiques à la Tunisie"""
        try:
            prompt = f"""
            En tant qu'expert de la Tunisie, donnez-moi des recommandations pour la catégorie : {category}
            
            Préférences spécifiées : {preferences if preferences else 'Aucune'}
            
            Fournissez :
            1. 3-5 recommandations détaillées
            2. Pourquoi ces choix sont excellents
            3. Conseils pratiques pour la visite
            4. Informations culturelles pertinentes
            
            Répondez en français de manière structurée et engageante.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Impossible de générer des recommandations pour {category}. Erreur: {str(e)}"
    
    def plan_tunisian_trip(self, duration, interests, budget, season):
        """Planifie un voyage en Tunisie personnalisé"""
        try:
            prompt = f"""
            Créez un itinéraire de voyage personnalisé pour la Tunisie :
            
            Durée : {duration} jours
            Intérêts : {interests}
            Budget : {budget}
            Saison : {season}
            
            Créez un planning détaillé avec :
            1. Itinéraire jour par jour
            2. Lieux à visiter avec explications
            3. Restaurants recommandés
            4. Conseils pratiques (transport, hébergement)
            5. Budget estimé
            6. Conseils culturels et de sécurité
            
            Répondez en français de manière structurée et engageante.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Impossible de planifier le voyage. Erreur: {str(e)}"
    
    def explain_tunisian_culture(self, topic):
        """Explique un aspect de la culture tunisienne"""
        try:
            prompt = f"""
            Expliquez en détail l'aspect culturel tunisien suivant : {topic}
            
            Incluez :
            1. Contexte historique
            2. Importance culturelle
            3. Traditions actuelles
            4. Conseils pour les visiteurs
            5. Anecdotes intéressantes
            
            Répondez en français de manière engageante et informative.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Impossible d'expliquer {topic}. Erreur: {str(e)}" 