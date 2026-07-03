import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        filepath = os.path.abspath("Presentation_Script.html")
        print(f"Generating PDF from: {filepath}")
        await page.goto(f"file://{filepath}")
        await page.emulate_media(media="print")
        await page.pdf(path="Presentation_Script.pdf", format="A4", print_background=True)
        await browser.close()
        print("Success: Presentation_Script.pdf generated.")

if __name__ == "__main__":
    asyncio.run(main())
