# Trip_planner_agent_mcp_server
Streamlit-based AI travel planner using multi-agent MCP architecture. Integrates Airbnb MCP for real-time stays and Google Maps MCP for precise distances. Delivers detailed itineraries with costs, buffer times, weather, dining, and attractions, plus calendar export and budget insights.

# 🧳 MCP Travel Planner Agent Team  

A sophisticated **Streamlit-based AI travel planning application** that creates extremely detailed, personalized itineraries using **multiple MCP servers** and **Google Maps integration**.  

The app leverages:  
- **Airbnb MCP** for real accommodation data  
- **Custom Google Maps MCP** for precise distance calculations and navigation  
- **Google Search tools** for weather, restaurants, attractions, and local insights  

---

## ✨ Features  

### 🤖 AI-Powered Travel Planning  
- **Extremely Detailed Itineraries**: Day-by-day schedules with specific timings, addresses, and costs  
- **Distance Calculations**: Google Maps MCP calculates precise travel times between locations  
- **Real-Time Accommodation Data**: Airbnb MCP provides current pricing and availability  
- **Personalized Recommendations**: Tailored itineraries based on preferences and budget  

### 🏨 Airbnb MCP Integration  
- Live accommodation listings with current pricing  
- Property details: amenities, reviews, booking availability  
- Budget-conscious recommendations filtered by location and preferences  
- Direct booking details with real-time rates  

### 🗺️ Google Maps MCP Integration  
- Precise distance and travel time calculations  
- Location services for POIs and navigation  
- Address verification for all recommendations  
- Transportation optimization with turn-by-turn guidance  

### 🔍 Google Search Integration  
- **Weather forecasts** with clothing suggestions  
- **Restaurant research** with addresses, price ranges, reviews  
- **Attraction insights**: hours, ticket prices, best visiting times  
- **Local tips**: culture, safety, currency exchange  

### 📅 Additional Features  
- **Calendar Export**: Download itinerary as `.ics` for Google, Apple, or Outlook  
- **Comprehensive Cost Breakdown** for all trip components  
- **Buffer Time Planning** for delays and transitions  
- **Multiple Accommodation Options** with distances from city center  

---

## ⚙️ Setup  

### Requirements  
- **Python 3.8+**  
- **API Keys**:  
  - OpenAI API Key → [Get here](https://platform.openai.com/)  
  - Google Maps API Key → [Get here](https://console.cloud.google.com/)  

### MCP Servers  
- **Airbnb MCP Server** → Real Airbnb listings & pricing  
- **Custom Google Maps MCP** → Distance calculations & location services  

### Installation  
```bash
# Clone repository
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/mcp_ai_agents/ai_travel_planner_mcp_agent_team

# Install dependencies
pip install -r requirements.txt
