import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Les Menuires Snow Hub", page_icon="❄️")

# Mapping weather codes to emojis
WEATHER_MAP = {
    0: "☀️ Clear", 1: "🌤️ Mostly Clear", 2: "⛅ Partly Cloudy", 3: "☁️ Overcast",
    71: "❄️ Light Snow", 73: "❄️ Snow", 75: "❄️ Heavy Snow", 85: "🌨️ Snow Showers"
}

def get_mountain_data():
    # Pointe de la Masse coordinates
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.32&longitude=6.54&current=temperature_2m,snowfall,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,snowfall_sum&timezone=Europe%2FBerlin"
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

st.title("🏔️ Les Menuires Snow Hub")

data = get_mountain_data()

if data:
    # --- SECTION 1: CURRENT & TODAY'S RANGE ---
    curr = data['current']
    today_min = data['daily']['temperature_2m_min'][0]
    today_max = data['daily']['temperature_2m_max'][0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Temp", f"{curr['temperature_2m']}°C")
    with col2:
        st.metric("Today's Range", f"{today_min}°C / {today_max}°C")
    with col3:
        condition = WEATHER_MAP.get(curr['weather_code'], "☁️ Cloudy")
        st.metric("Status", condition)

    # --- SECTION 2: LIVE VIEW ---
    st.markdown("[📸 View Official Live Webcams](https://lesmenuires.com/en/webcams)")

    # --- SECTION 3: POWDER ALERT ---
    tomorrow_snow = data['daily']['snowfall_sum'][1]
    if tomorrow_snow > 10:
        st.info(f"🚨 **POWDER ALERT:** {tomorrow_snow}cm of fresh snow expected tomorrow!")

    # --- SECTION 4: 7-DAY FORECAST ---
    st.write("### 📅 7-Day Forecast")
    df = pd.DataFrame({
        "Day": data['daily']['time'],
        "Condition": [WEATHER_MAP.get(c, "☁️") for c in data['daily']['weather_code']],
        "Min Temp": [f"{t}°C" for t in data['daily']['temperature_2m_min']],
        "Max Temp": [f"{t}°C" for t in data['daily']['temperature_2m_max']],
        "New Snow": [f"{s}cm" for s in data['daily']['snowfall_sum']]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.error("Mountain sensors are offline. Try again in a minute!")

if st.button('🔄 Refresh Data'):
    st.rerun()
