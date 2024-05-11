from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os
from selenium.webdriver.chrome.service import Service


# Get the current timestamp for the image name
image_name = "standard_screenshot"


service = Service(executable_path='/Users/vasileadrianfeier/Downloads/chromedriver-mac-arm64/chromedriver')

# Configure Chrome WebDriver options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--headless")  # Use headless mode for running in the background
options.add_argument("--disable-gpu")
options.add_argument("--disable-cookies")


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service,
                          options=options)
driver.maximize_window()

# Navigate to the URL you want to capture
#driver.get("https://greenzy.eu/en/")
#driver.get("https://effixis.ch/")
#driver.get("https://en.wikipedia.org/wiki/Vanessa_Paradis")
driver.get("https://www.mersen.com/")
#driver.get("https://www.nba.com/standings")
#driver.get("https://www.espn.com/nba/standings")

cookies_disabled = driver.execute_script('return document.cookie')
if not cookies_disabled:
    print("Cookies are disabled.")
else:
    print("Cookies are enabled.")  # This should not be reached if cookies are truly disabled


# Wait for the page to load (you can adjust the sleep time as needed)
time.sleep(2)

# Use JavaScript to get the full width and height of the webpage
width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

# Set the window size to match the entire webpage
driver.set_window_size(width, height)

# Find the full page element (usually 'body') and capture the screenshot
full_page = driver.find_element(By.TAG_NAME, "body")
full_page.screenshot(f"{image_name}.png")

# analyse the screenshot

## is there any Captcha ?

## is there any cookie banner ?


# Close the browser window
driver.quit()
