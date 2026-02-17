import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Les Menuires Snow Hub", page_icon="❄️", layout="wide")

# Weather code mapping (WMO standards)
WEATHER_CODES = {
    0: "☀️ Clear sky", 1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
    71: "❄️ Slight snowfall", 73: "❄️ Moderate snowfall", 75: "❄️ Heavy snowfall",
    77: "🌨️ Snow grains", 85: "❄️ Slight snow showers", 86: "❄️ Heavy snow showers"
}

def get_resort_data():
    lat, lon = 45.32, 6.54
    # Fetching both current and 7-day daily forecast
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,snowfall,weather_code&daily=temperature_2m_max,temperature_2m_min,snowfall_sum,weather_code&timezone=Europe%2FBerlin"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return None

st.title("🏔️ Les Menuires Snow & Forecast")

data = get_resort_data()

if data:
    # --- TOP ROW: CURRENT CONDITIONS ---
    curr = data['current']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Temp", f"{curr['temperature_2m']}°C")
    with col2:
        condition = WEATHER_CODES.get(curr['weather_code'], "☁️ Cloudy")
        st.metric("Condition", condition)
    with col3:
        st.metric("Recent Snow", f"{curr['snowfall']} cm")

    st.divider()

    # --- BOTTOM ROW: 7-DAY FORECAST ---
    st.subheader("📅 7-Day Mountain Forecast")
    
    daily = data['daily']
    forecast_df = pd.DataFrame({
        "Date": daily['time'],
        "Max Temp": [f"{t}°C" for t in daily['temperature_2m_max']],
        "Min Temp": [f"{t}°C" for t in daily['temperature_2m_min']],
        "New Snow": [f"{s} cm" for s in daily['snowfall_sum']],
        "Conditions": [WEATHER_CODES.get(code, "☁️ Cloudy") for code in daily['weather_code']]
    })
    
    # Display the table
    st.table(forecast_df)
    
    st.caption(f"Elevation: {data.get('elevation', '1850')}m | Data via Open-Meteo")

else:
    st.error("Could not fetch the latest mountain data. Please try again in a moment.")

if st.button('🔄 Refresh Dashboard'):
    st.rerun()
