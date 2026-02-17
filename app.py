import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.title("❄️ Les Menuires Live Snow")

def get_snow_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://lesmenuires.com/en/live")
        
        # Wait up to 15 seconds for the snow info to actually appear
        wait = WebDriverWait(driver, 15)
        
        # We search for the specific text labels to find the numbers next to them
        # This is more stable than using random class names
        try:
            # Finding the "Snow bottom" and "Snow top" values
            # The site uses 'm-weather-infos__value' inside a weather block
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "m-weather-infos__value")))
            
            # Usually: Index 0 is Bottom, Index 1 is Top
            if len(elements) >= 2:
                res = {
                    "Station (1850m)": elements[0].text,
                    "Summit (2800m)": elements[1].text
                }
            else:
                res = "Found the page, but the snow numbers haven't loaded yet."
        except Exception:
            res = "Timeout: The snow data didn't appear in time."

        driver.quit()
        return res
    except Exception as e:
        return f"Connection Error: {e}"

if st.button('Refresh Snow Report'):
    with st.spinner('Digging through the snow...'):
        data = get_snow_data()
        if isinstance(data, dict):
            st.balloons() # Just for fun when it works!
            col1, col2 = st.columns(2)
            col1.metric("Station (1850m)", data["Station (1850m)"])
            col2.metric("Summit (2800m)", data["Summit (2800m)"])
        else:
            st.error(data)
