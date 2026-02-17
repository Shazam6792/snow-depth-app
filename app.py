import streamlit as st
import requests

st.set_page_config(page_title="Les Menuires Snow", page_icon="❄️")
st.title("❄️ Les Menuires Live Snow")

def get_snow_report():
    # This is the direct data feed used by the 3 Vallées apps
    url = "https://api.les3vallees.com/api/v1/resorts/les-menuires/weather"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Navigating the JSON structure
        # Note: If the API structure changes, we just update these keys
        snow_bottom = data.get('snow', {}).get('bottom', 'N/A')
        snow_top = data.get('snow', {}).get('top', 'N/A')
        last_update = data.get('updated_at', 'Recently')
        
        return {
            "bottom": f"{snow_bottom} cm",
            "top": f"{snow_top} cm",
            "update": last_update
        }
    except Exception as e:
        return f"API Error: {e}"

# Display Logic
if st.button('Update Now'):
    result = get_snow_report()
    if isinstance(result, dict):
        col1, col2 = st.columns(2)
        col1.metric("Station (1850m)", result["bottom"])
        col2.metric("Summit (2800m)", result["top"])
        st.caption(f"Last updated: {result['update']}")
    else:
        st.error("Could not reach the mountain data. The API might be down.")
else:
    st.info("Click the button to pull live data from the 3 Vallées server.")
