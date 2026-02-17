import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Les Menuires Snow", page_icon="❄️")
st.title("❄️ Les Menuires Snow Report")

def get_snow_depth():
    # GPS Coordinates for Les Menuires
    lat = 45.32
    lon = 6.54
    
    # Open-Meteo API (Free, no key needed)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=snowfall_sum,shortwave_radiation_sum&current_weather=true&hourly=snow_depth&timezone=Europe%2FBerlin"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Get the current snow depth from the hourly data
        # Open-Meteo provides estimated snow depth based on weather models
        current_depth_m = data['hourly']['snow_depth'][0] 
        current_depth_cm = current_depth_m * 100 # Convert meters to cm
        
        return {
            "depth": f"{int(current_depth_cm)} cm",
            "temp": f"{data['current_weather']['temperature']}°C",
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except Exception as e:
        return f"Error: {e}"

if st.button('Get Live Data'):
    with st.spinner('Accessing weather satellites...'):
        result = get_snow_depth()
        if isinstance(result, dict):
            st.balloons()
            col1, col2 = st.columns(2)
            col1.metric("Current Snow Depth", result["depth"])
            col2.metric("Current Temp", result["temp"])
            st.caption(f"Last updated at: {result['time']}")
        else:
            st.error(result)
else:
    st.info("Click the button to get the model-calculated snow depth.")
