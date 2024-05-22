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

from app.services.gpt_vision_service import get_content_with_Vision

# Navigate to the URL you want to capture
    #name = "Greenzy"
    #urls= {
    #"Greenzy": "https://greenzy.eu/en/", #- OK
    #"Effixis":"https://effixis.ch/", #- NOK
    #"Wiki": "https://en.wikipedia.org/wiki/Vanessa_Paradis", #- OK with and without agent
    #"Mersen": "https://www.mersen.com/", #- OK with and without agent
    #"NBA": "https://www.nba.com/standings", #- OK with agent
    #"ESPN": "https://www.espn.com/nba/standings", #- NOK because no cookie banner
    #"ATP": "https://www.atptour.com/en" # - OK with and without agent because cookie banner not blocking
    #}


async def take_screenshot(url, info):

    # Get the current timestamp for the image name
    image_name = f"standard_screenshot_{url}"

    full_options = create_driver_options_with_Mozilla()
    driver = get_driver_for_url(full_options)
    buttons = get_buttons_with_Mozilla(driver)

    # if the list of buttons is empty, try to add the agent
    # TODO: investigate ways to detect Captchas
    if not buttons:
        options = create_driver_options()
        driver = get_driver_for_url(options)
        buttons = get_buttons(driver)

    # if the buttons is not empty, click on accept button
    else:
        ## Ask GPT to select the right button
        agree_button = await select_accept_button(buttons)

        ## Click on Accept cookie button
        if len(agree_button)>2:
            click_on_accept_button(driver, agree_button)

    take_screenshot_with_driver(driver, image_name)

    driver.quit()

    return get_content_with_Vision(f"./{image_name}.png", info)

def take_screenshot_with_driver(driver, image_name):
    width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
    height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    driver.set_window_size(width, height)

    # Find the full page element (usually 'body') and capture the screenshot
    full_page = driver.find_element(By.TAG_NAME, "body")
    full_page.screenshot(f"{image_name}.png")

def click_on_accept_button(driver, agree_button):
    driver.find_element(by=By.XPATH, value=f"""//button[contains(text(), "{agree_button}")]""").click()

def get_buttons_from_driver(driver):
    return [button.text for button in driver.find_elements(By.TAG_NAME, "button") if button.text!=""]

def get_buttons(driver):
    return get_buttons_from_driver(driver)

def get_buttons_with_Mozilla(driver):
    return get_buttons_from_driver(driver)


# TODO: make the function async by replacing the get
async def get_driver_for_url(options, url):

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

    driver.get(url)

    return driver


def create_driver_options():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    return options

def create_driver_options_with_Mozilla():

    options = create_driver_options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    return options



async def select_accept_button(buttons_list):
    prompt = f"""You are given a list of buttons.
    Do not output your reasoning.
    You are asked to select the button that allows me to accept cookies settings.
    If there is no such button, output an empty string.
    Here is the list of buttons: {buttons_list}.
    """

    gpt_answer = await get_gpt_4_completion(prompt)

    return gpt_answer


if __name__ == "__main__":
    start_time = time.time()
    info = asyncio.run(take_screenshot())
    print(info)
    print("--- %s seconds ---" % (time.time() - start_time))
