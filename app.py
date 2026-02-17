import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Les Menuires Snow", page_icon="❄️")
st.title("❄️ Les Menuires Snow Report")

def get_snow_depth():
    # We use Snow-Forecast as it's more stable for automation
    url = "https://www.snow-forecast.com/resorts/Les-Menuires/snow-report"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the snow depth values in the table
        # We look for the "Upper" and "Lower" depth classes
        depths = soup.find_all("span", class_="depth")
        
        if len(depths) >= 2:
            return {
                "Upper (2800m)": depths[0].get_text() + " cm",
                "Lower (1850m)": depths[1].get_text() + " cm"
            }
        else:
            return "Could not find depths. Site structure might have changed."
    except Exception as e:
        return f"Error: {e}"

if st.button('Refresh Data'):
    with st.spinner('Checking the mountain...'):
        data = get_snow_depth()
        if isinstance(data, dict):
            st.balloons()
            col1, col2 = st.columns(2)
            col1.metric("Station (1850m)", data["Lower (1850m)"])
            col2.metric("Summit (2800m)", data["Upper (2800m)"])
            st.success("Updated for Feb 2026!")
        else:
            st.error(data)
else:
    st.info("Click the button to fetch the latest snow depths.")
