import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        filepath = os.path.abspath("Weekly_Meeting_11.html")
        await page.goto(f"file://{filepath}")
        await page.wait_for_timeout(2000)  # wait for Google Fonts to load
        await page.emulate_media(media="print")
        
        # Output directly to the associated team meeting folder
        output_path = os.path.abspath("../Team22 - Weekly Meeting/team22_Weekly_Meeting_11.pdf")
        print(f"Generating PDF to: {output_path}")
        
        await page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        await browser.close()
        print("✅ team22_Weekly_Meeting_11.pdf generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
