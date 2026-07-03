import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Get absolute file URL
        filepath = os.path.abspath("Startup_Charter.html")
        await page.goto(f"file://{filepath}")
        await page.emulate_media(media="print")
        await page.pdf(path="Startup_Charter_CleanTech.pdf", format="A4", print_background=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
