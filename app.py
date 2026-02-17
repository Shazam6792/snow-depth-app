import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

st.title("❄️ Les Menuires Snow Report")

def get_snow_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # This makes the "robot" look like a real Chrome browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://lesmenuires.com/en/live")
        
        # Wait for the dynamic data to load
        time.sleep(5)
        
        # Finding the depth values
        elements = driver.find_elements(By.CLASS_NAME, "m-weather-infos__value")
        
        if len(elements) >= 2:
            res = {
                "Station (1850m)": elements[0].text,
                "Summit (2800m)": elements[1].text
            }
        else:
            res = "Data not found. The site might be under maintenance."
            
        driver.quit()
        return res
    except Exception as e:
        return f"Error: {e}"

if st.button('Update Snow Depth'):
    with st.spinner('Checking the mountain...'):
        data = get_snow_data()
        if isinstance(data, dict):
            col1, col2 = st.columns(2)
            col1.metric("Station (1850m)", data["Station (1850m)"])
            col2.metric("Summit (2800m)", data["Summit (2800m)"])
            st.success("Last updated just now!")
        else:
            st.error(data)
else:
    st.write("Click the button to fetch live data.")
