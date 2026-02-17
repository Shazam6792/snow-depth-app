import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Les Menuires Snow Hub", page_icon="❄️")

# Mapping weather codes to emojis
WEATHER_MAP = {
    0: "☀️ Clear", 1: "🌤️ Mostly Clear", 2: "⛅ Partly Cloudy", 3: "☁️ Overcast",
    71: "❄️ Light Snow", 73: "❄️ Snow", 75: "❄️ Heavy Snow", 85: "🌨️ Snow Showers"
}

def get_mountain_data():
    # Pointe de la Masse coordinates
    # We added 'snow_depth' to the hourly request
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.32&longitude=6.54&current=temperature_2m,snowfall,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,snowfall_sum&hourly=temperature_2m,snow_depth&timezone=Europe%2FBerlin"
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

st.title("🏔️ Les Menuires Snow Hub")

data = get_mountain_data()

if data:
    # --- SECTION 1: TOP METRICS ---
    curr = data['current']
    
    # Get the very latest snow depth from the hourly list (converted from meters to cm)
    current_depth_cm = data['hourly']['snow_depth'][0] * 100 
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Snow Depth", f"{int(current_depth_cm)} cm")
    with col2:
        st.metric("Current Temp", f"{curr['temperature_2m']}°C")
    with col3:
        condition = WEATHER_MAP.get(curr['weather_code'], "☁️ Cloudy")
        st.metric("Status", condition)

    # --- SECTION 2: 24-HOUR TREND ---
    st.write("### 📈 24-Hour Temperature Trend")
    hourly_times = [datetime.fromisoformat(t).strftime("%H:%M") for t in data['hourly']['time'][:24]]
    hourly_temps = data['hourly']['temperature_2m'][:24]
    
    chart_data = pd.DataFrame({
        "Time": hourly_times,
        "Temp (°C)": hourly_temps
    }).set_index("Time")
    
    st.line_chart(chart_data)

    # --- SECTION 3: 7-DAY FORECAST ---
    st.write("### 📅 7-Day Forecast")
    df = pd.DataFrame({
        "Day": data['daily']['time'],
        "Condition": [WEATHER_MAP.get(c, "☁️") for c in data['daily']['weather_code']],
        "Min": [f"{t}°C" for t in data['daily']['temperature_2m_min']],
        "Max": [f"{t}°C" for t in data['daily']['temperature_2m_max']],
        "New Snow": [f"{s}cm" for s in data['daily']['snowfall_sum']]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("[📸 View Official Live Webcams](https://lesmenuires.com/en/webcams)")

else:
    st.error("Mountain sensors are offline. Try again in a minute!")

if st.button('🔄 Refresh Data'):
    st.rerun()
