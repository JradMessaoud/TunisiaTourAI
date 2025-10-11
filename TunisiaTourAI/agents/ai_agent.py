import os
import time
import streamlit as st
import google.generativeai as genai
from utils.cache_manager import cached_response, cache_manager
from utils.logger import get_logger

class AIAgent:
    def __init__(self):
        """Initialize the AI agent with Tunisia-specific context (English prompts)."""
        # Get API key from Streamlit secrets
        self.api_key = st.secrets.get("GEMINI_API_KEY")

        # Show API status in the sidebar (English)
        if self.api_key:
            st.sidebar.success("🤖 Gemini AI: ✅ Configured")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.is_available = True
        else:
            st.sidebar.warning("🤖 Gemini AI: ❌ Not configured")
            self.is_available = False
            self.model = None

        # English system context specialized for Tunisia
        self.tunisian_context = """
        You are TunisiaTourAI — an expert specialized in tourism, culture, history, and traditions of Tunisia.

        Your role:
        - ANSWER ONLY questions related to Tunisia.
        - Provide accurate information about destinations, monuments, festivals, culture, gastronomy, history and traditions.
        - Give practical travel advice for Tunisia.
        - Recommend itineraries and activities within Tunisia.
        - Explain Tunisian customs and traditions.

        If a question is not about Tunisia, politely redirect the user back to Tunisia-related topics, for example:
        "I specialize in Tunisia. May I help you with questions about Tunisian destinations, monuments, festivals, or culture?"

        Always respond in English in a detailed, engaging, and informative manner.
        Include cultural, historical and practical details when relevant.
        """

        # Initialize logger
        self.logger = get_logger()

    @cached_response
    def ask(self, question, context=None):
        """Ask the model a question with Tunisia context (cached & logged). Returns English text."""
        start_time = time.time()

        if not self.is_available or self.model is None:
            return "⚠️ Gemini AI is not configured. Please set GEMINI_API_KEY in Streamlit secrets."

        try:
            # Build the prompt in English
            if context:
                full_prompt = f"{self.tunisian_context}\n\nContext: {context}\n\nQuestion: {question}\n\nPlease respond in English, structured and concise."
            else:
                full_prompt = f"{self.tunisian_context}\n\nQuestion: {question}\n\nPlease respond in English, structured and concise."

            # Call the model
            response = self.model.generate_content(full_prompt)
            response_text = response.text

            # Log successful request
            duration = time.time() - start_time
            self.logger.log_ai_request(question, response_text, duration, True)

            return response_text

        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_ai_request(question, str(e), duration, False)

            err_str = str(e).lower()
            if "quota" in err_str or "429" in err_str:
                return ("⚠️ You have exceeded Gemini AI usage limits. "
                        "Please wait a few minutes or generate a new API key at https://aistudio.google.com/app/apikey.")
            return f"Sorry, I'm experiencing a technical issue. Please try again later. Error: {str(e)}"

    def get_tunisian_recommendation(self, category, preferences=None):
        """Get Tunisia-specific recommendations (English)."""
        if not self.is_available or self.model is None:
            return "⚠️ Gemini AI is not configured."

        try:
            prompt = f"""
            As a Tunisia expert, provide recommendations for the category: {category}

            Preferences specified: {preferences if preferences else 'None'}

            Provide:
            1) 3-5 detailed recommendations
            2) Why these choices are excellent
            3) Practical tips for visiting
            4) Relevant cultural information

            Respond in English, structured and engaging.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate recommendations for {category}. Error: {str(e)}"

    def plan_tunisian_trip(self, duration, interests, budget, season):
        """Plan a personalized Tunisia trip (English)."""
        if not self.is_available or self.model is None:
            return "⚠️ Gemini AI is not configured."

        try:
            prompt = f"""
            Create a customized travel itinerary for Tunisia with these parameters:

            Duration: {duration} days
            Interests: {interests}
            Budget: {budget}
            Season: {season}

            Provide:
            1) Day-by-day schedule with suggested times
            2) Places to visit with descriptions
            3) Recommended restaurants
            4) Practical tips (transport, accommodation)
            5) Estimated daily budget
            6) Cultural and safety advice

            Respond in English, structured and engaging.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to plan the trip. Error: {str(e)}"

    def explain_tunisian_culture(self, topic):
        """Explain an aspect of Tunisian culture (English)."""
        if not self.is_available or self.model is None:
            return "⚠️ Gemini AI is not configured."

        try:
            prompt = f"""
            Explain in detail the following Tunisian cultural topic: {topic}

            Include:
            1) Historical context
            2) Cultural significance
            3) Current traditions
            4) Visitor tips
            5) Interesting anecdotes

            Respond in English, engaging and informative.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to explain {topic}. Error: {str(e)}"
