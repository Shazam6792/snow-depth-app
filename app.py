import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_snow_depth():
    # Setup headless browser (no window pops up)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    url = "https://lesmenuires.com/en/live"
    
    try:
        driver.get(url)
        time.sleep(5) # Give the page time to load the live data
        
        # Look for the snow depth elements
        # Note: These selectors may need updating if the website layout changes
        snow_depths = driver.find_elements(By.CLASS_NAME, "m-weather-infos__value")
        
        if snow_depths:
            # Usually: [0] is Station (1850m), [1] is Summit (2850m)
            station_depth = snow_depths[0].text
            summit_depth = snow_depths[1].text
            
            print(f"❄️ Les Menuires Snow Report ❄️")
            print(f"Station (1850m): {station_depth}")
            print(f"Summit (2800m): {summit_depth}")
        else:
            print("Could not find snow depth data. The site structure might have changed.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    get_snow_depth()
