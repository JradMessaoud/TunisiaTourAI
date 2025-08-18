
# 🇹🇳 TunisiaTourAI

**Your intelligent guide to discovering the beauty and richness of Tunisia**  

A modern **Streamlit application** that combines **artificial intelligence** with a complete database of Tunisia’s **destinations, monuments, and festivals**.  

🌐 Live Demo: [TunisiaTourAI](https://tunisiatourai.streamlit.app/)  
📂 Repository: https://github.com/JradMessaoud/TunisiaTourAI  

---

## ✨ Features

### 🏖️ Destinations
- 15 destinations covering all Tunisian regions  
- Authentic images from Wikimedia Commons  
- Filters by region and type  
- Personalized AI reviews  
- Favorites system  

### 🗿 Monuments
- 18 historical and cultural monuments  
- Archaeological and religious sites  
- Detailed descriptions with historical context  
- AI visit recommendations  

### 🎉 Festivals
- 19 cultural festivals and seasonal events  
- Complete yearly calendar  
- Practical and cultural information  
- Traditional and modern celebrations  

### 🤖 Tunisian AI Assistant
- Powered by **Gemini 2.0 Flash**  
- Specialized exclusively in Tunisia  
- Detailed and engaging answers (in French)  
- Smart caching system for performance  

### 🗺️ Travel Planner
- Interactive trip planner  
- Customizable (duration, budget, interests)  
- AI-generated itineraries  
- Popular itinerary examples  

### ❤️ Favorites
- Save and organize your favorite places  
- Category-based management  
- Persistent storage  

---

## 🚀 New in v2.0

- ⚡ **Performance Optimizations** (caching, faster image loading, fewer API calls)  
- 📊 **Monitoring & Logs** (full logging, usage stats, performance tracking)  
- 🎨 **Enhanced UI** (modern Tunisian theme, animations, responsive design)  

---

## 🛠️ Installation

### Requirements
- Python 3.8+  
- Gemini API Key (Google AI Studio)  

### Setup
```bash
# Clone the repository
git clone https://github.com/JradMessaoud/TunisiaTourAI
cd TunisiaTourAI

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GEMINI_API_KEY=your_api_key" > .env

# Run the app
streamlit run TunisiaTourAI/app.py
````

---

## 📁 Project Structure

```
TunisiaTourAI/
├── TunisiaTourAI/
│   ├── app.py                 # Main app
│   ├── config.py              # Global config
│   ├── agents/
│   │   └── ai_agent.py        # AI agent with cache + logs
│   ├── pages/
│   │   ├── 1_🏖️_Destinations.py
│   │   ├── 2_🗿_Monuments.py
│   │   ├── 3_🎉_Festivals.py
│   │   ├── 4_🤖_ChatWithAI.py
│   │   ├── 5_🗺️_Planner.py
│   │   └── 6_❤️_Favorites.py
│   └── utils/
│       ├── cache_manager.py
│       ├── favorites_manager.py
│       └── logger.py
├── images/                    
├── cache/                     
├── logs/                      
├── favorites.json             
└── requirements.txt
```

---

## 🎯 Usage

* **Home** → Overview + Quick AI chat
* **Destinations** → Explore Tunisia by region/type
* **Monuments** → Discover history and heritage
* **Festivals** → Cultural events and traditions
* **Planner** → Build your itinerary
* **Favorites** → Manage saved places
* **AI Chat** → Ask anything about Tunisia

---

## 🔧 Configuration

Edit `config.py` to customize:

* Theme colors
* Cache settings
* AI behavior
* Regions & categories

---

## 📊 Stats

* 15 destinations
* 18 monuments
* 19 festivals
* 32 authentic images
* AI caching + full logging

---

## 📝 Roadmap

* [ ] Interactive maps
* [ ] Dark mode
* [ ] Ratings & reviews
* [ ] Multilingual support
* [ ] Export itineraries to PDF
* [ ] Real-time weather
* [ ] Notifications

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repo
2. Create a new branch
3. Commit changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Developer

Developed with ❤️ for Tunisia by **Messaoud Jrad**

* [LinkedIn](https://www.linkedin.com/in/massoud-jrad-1a9250321/)
* [GitHub](https://github.com/JradMessaoud)

---

🌍 **TunisiaTourAI – Your intelligent guide to discover Tunisia.**

