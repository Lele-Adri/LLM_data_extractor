from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, asyncio, requests

from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs

from app.helpers.llm_helpers import get_gpt_4_completion

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth

import re


async def take_screenshot():

    #service = Service(executable_path='/Users/vasileadrianfeier/Downloads/chromedriver-mac-arm64/chromedriver')

    # Configure Chrome WebDriver options hihi
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)


    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    stealth(driver,
       user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
       )



    # Navigate to the URL you want to capture
    name = "ATP"
    urls= {
    "Greenzy": "https://greenzy.eu/en/", #- OK
    "Effixis":"https://effixis.ch/", #- NOK
    "Wiki": "https://en.wikipedia.org/wiki/Vanessa_Paradis", #- OK with and without agent
    "Mersen": "https://www.mersen.com/", #- OK with and without agent
    "NBA": "https://www.nba.com/standings", #- OK with agent
    "ESPN": "https://www.espn.com/nba/standings", #- NOK because no cookie banner
    "ATP": "https://www.atptour.com/en" # - OK with and without agent because cookie banner not blocking
    }
    time.sleep(2)
    driver.get(urls[name])

    # Get the current timestamp for the image name
    image_name = "standard_screenshot-" + name

    # Accept cookies to make the cookie banner disappear
    time.sleep(2)
    # best solution: find all the buttons and select the good one
    buttons = [button.text for button in driver.find_elements(By.TAG_NAME, "button") if button.text!=""]

    # other solution: find all <a> tags with class name containing "button" and select the good one
    #soup = bs(driver.page_source, 'html.parser')

    #links = soup.find_all('a', {'class': re.compile(r'button')})
    #for element in links:
    #    print(element.get_text())

    print(buttons)

    # if the list of buttons is empty, try to add the agent
    if not buttons:
        time.sleep(2)
        print("Enter Not Buttons option")
        options.arguments.remove("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        driver = webdriver.Chrome(options=options)
        stealth(driver,
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

        driver.get(urls[name])
        time.sleep(2)
        buttons = [button.text for button in driver.find_elements(By.TAG_NAME, "button") if button.text!=""]

        print("Here are the new buttons:")
        print(buttons)

    # if the buttons is not empty, click on accept button
    if buttons:
        time.sleep(2)
        ## Ask GPT to select the right button
        agree_button = await select_button(buttons)
        print("Here is the agree button:")
        print(agree_button)

        ## Click on Accept cookie button
        if len(agree_button)>2:
            time.sleep(2)
            driver.find_element(by=By.XPATH, value=f"""//button[contains(text(), "{agree_button}")]""").click()
            time.sleep(2)

    # Use JavaScript to get the full width and height of the webpage
    width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
    height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    time.sleep(2)
    # Set the window size to match the entire webpage
    driver.set_window_size(width, height)
    time.sleep(2)

    # Find the full page element (usually 'body') and capture the screenshot
    full_page = driver.find_element(By.TAG_NAME, "body")
    full_page.screenshot(f"{image_name}.png")

    # analyse the screenshot

    ## is there any Captcha ?

    ## is there any cookie banner ?


    # Close the browser window
    driver.quit()
    return 1


async def select_button(buttons_list):
    prompt = f"""You are given a list of buttons.
    Do not output your reasoning.
    You are asked to select the button that allows me to accept cookies settings.
    If there is no such button, output an empty string.
    Here is the list of buttons: {buttons_list}.
    """

    gpt_answer = await get_gpt_4_completion(prompt)

    return gpt_answer


if __name__ == "__main__":
    asyncio.run(take_screenshot())
