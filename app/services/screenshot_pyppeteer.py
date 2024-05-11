import asyncio
from pyppeteer import launch
import time

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto("https://www.nba.com/standings")
    # Wait for the page to load (you can adjust the sleep time as needed)
    time.sleep(2)
    await page.screenshot({'path': 'pyppeterr_screenshot.png', 'fullPage': True})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
