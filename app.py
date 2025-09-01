import asyncio
import os

from agno.agent import Agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from agno.team.team import Team
from agno.tools.mcp import MultiMCPTools
import streamlit as st
from datetime import date
import logging
logging.getLogger("httpx").setLevel(logging.ERROR)

from groq._base_client import SyncHttpxClientWrapper

def safe_del(self):
    try:
        if hasattr(self, 'is_closed') and self.is_closed:
            pass
    except Exception:
        pass

SyncHttpxClientWrapper.__del__ = safe_del

async def run_agent(message: str)-> str:
    """Run the travel planner agents using Groq's LLaMA model."""

    # Get API keys from session state
    google_maps_key = st.session_state.get('google_maps_key')
    accuweather_key = st.session_state.get('accuweather_key')
    groq_key = st.session_state.get('groq_key')
    google_client_id = st.session_state.get('google_client_id')
    google_client_secret = st.session_state.get('google_client_secret')
    google_refresh_token = st.session_state.get('google_refresh_token')

    if not google_maps_key:
        raise ValueError("🚨 Missing Google Maps API Key. Please enter it in the sidebar.")
    elif not accuweather_key:
        raise ValueError("🚨 Missing AccuWeather API Key. Please enter it in the sidebar.")
    elif not groq_key:
        raise ValueError("🚨 Missing Groq API Key. Please enter it in the sidebar.")
    elif not google_client_id:
        raise ValueError("🚨 Missing Google Client ID. Please enter it in the sidebar.")
    elif not google_client_secret:
        raise ValueError("🚨 Missing Google Client Secret. Please enter it in the sidebar.")
    elif not google_refresh_token:
        raise ValueError("🚨 Missing Google Refresh Token. Please enter it in the sidebar.")
    # Set environment variables for MCP tools
    env = {
        **os.environ,
        "GOOGLE_MAPS_API_KEY": google_maps_key,
        "ACCUWEATHER_API_KEY": accuweather_key,
        "GOOGLE_CLIENT_ID": google_client_id,
        "GOOGLE_CLIENT_SECRET": google_client_secret,
        "GOOGLE_REFRESH_TOKEN": google_refresh_token
    }

    async with MultiMCPTools(
    [
        "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
        "npx -y @modelcontextprotocol/server-google-maps",
        "python3 ./mcp-weather/mcp_weather/weather.py",
        "python3 calendar_mcp.py"

    ],
    env=env,
)   as mcp_tools:
        

        model = ChatGroq(
            api_key=groq_key,
            model="llama3-70b-8192",
            temperature=0.1,
            max_tokens=1000
        )
        maps_agent = Agent(tools=[mcp_tools], model=model, name="Maps Agent", goal="""...""")  # same goals
        weather_agent = Agent(tools=[mcp_tools], model=model, name="Weather Agent", goal="""...""")
        booking_agent = Agent(tools=[mcp_tools], model=model, name="Booking Agent", goal="""...""")
        calendar_agent = Agent(tools=[mcp_tools], model=model, name="Calendar Agent", goal="""...""")

        team = Team(
            members=[maps_agent, weather_agent, booking_agent, calendar_agent],
            model=model,
            name="Travel Planning Team",
            markdown=True,
            show_tool_calls=True,
            instructions="""..."""  # full team instructions here
        )

        try:
            result = await team.arun(message)
            # print("Raw message (stringified):", str(result.messages[-1]))
            content = result.messages[-1].content
            if isinstance(content, str):
                return content
            else:
                return str(content)
        finally:
            import gc
            del team
            del maps_agent, weather_agent, booking_agent, calendar_agent
            del mcp_tools
            del model
            gc.collect()


# -------------------- Streamlit App --------------------

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

with st.sidebar:
    st.header("🔑 API Keys Configuration")

    keys = {
        "google_maps_key": "Google Maps API Key",
        "accuweather_key": "AccuWeather API Key",
        "groq_key": "Groq API Key",
        "google_client_id": "Google Client ID",
        "google_client_secret": "Google Client Secret",
        "google_refresh_token": "Google Refresh Token"
    }

    for key, label in keys.items():
        if key not in st.session_state:
            st.session_state[key] = ""
        st.session_state[key] = st.text_input(label, value=st.session_state[key], type="password")

    all_keys_filled = all(st.session_state[key] for key in keys)

    if all_keys_filled:
        st.success("✅ All API keys are configured!")
    else:
        st.warning("⚠️ Please fill in all API keys to use the travel planner.")

# -------------------- UI Layout --------------------

st.title("✈️ AI Travel Planner")
st.markdown("""
This AI-powered travel planner helps you create personalized travel itineraries using:
- 🗺️ Maps and navigation
- 🌤️ Weather forecasts
- 🏨 Accommodation booking
- 📅 Calendar management
""")

col1, col2 = st.columns(2)

with col1:
    source = st.text_input("Source", placeholder="Enter your departure city")
    destination = st.text_input("Destination", placeholder="Enter your destination city")
    travel_dates = st.date_input("Travel Dates", [date.today(), date.today()], min_value=date.today())

with col2:
    budget = st.number_input("Budget (in USD)", min_value=0, max_value=10000, step=100)
    travel_preferences = st.multiselect("Travel Preferences", [
        "Adventure", "Relaxation", "Sightseeing", "Cultural Experiences",
        "Beach", "Mountain", "Luxury", "Budget-Friendly", "Food & Dining",
        "Shopping", "Nightlife", "Family-Friendly"
    ])

st.subheader("Additional Preferences")
col3, col4 = st.columns(2)

with col3:
    accommodation_type = st.selectbox("Preferred Accommodation", ["Any", "Hotel", "Hostel", "Apartment", "Resort"])
    transportation_mode = st.multiselect("Preferred Transportation", ["Train", "Bus", "Flight", "Rental Car"])

with col4:
    dietary_restrictions = st.multiselect("Dietary Restrictions", [
        "None", "Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher"
    ])

async def main():
    if not source or not destination:
        st.error("Please enter both source and destination cities.")
    elif not travel_preferences:
        st.warning("Consider selecting some travel preferences for better recommendations.")
    else:
        with st.spinner("🤖 AI Agents are planning your perfect trip..."):
            try:
                message = f"""
                Plan a trip with the following details:
                - From: {source}
                - To: {destination}
                - Dates: {travel_dates[0]} to {travel_dates[1]}
                - Budget in USD: ${budget}
                - Preferences: {', '.join(travel_preferences)}
                - Accommodation: {accommodation_type}
                - Transportation: {', '.join(transportation_mode)}
                - Dietary Restrictions: {', '.join(dietary_restrictions)}
                
                Please provide a comprehensive travel plan including:
                1. Recommended accommodations
                2. Daily itinerary with activities
                3. Transportation options
                4. The Expected Day Weather
                5. Estimated cost of the Trip
                6. Add the Departure Date to the calendar
                """
                

                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    task = asyncio.ensure_future(run_agent(message))
                    response = await task
                else:
                    response = loop.run_until_complete(run_agent(message))
                st.success("✅ Your travel plan is ready!")
                try:
                    st.markdown(str(response))
                except Exception:
                    st.error("⚠️ Failed to display the response.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if st.button("Plan My Trip", type="primary", disabled=not all_keys_filled):
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(main())
    else:
        loop.run_until_complete(main())

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Powered by AI Travel Planning Agents</p>
    <p>Your personal travel assistant for creating memorable experiences</p>
</div>
""", unsafe_allow_html=True)