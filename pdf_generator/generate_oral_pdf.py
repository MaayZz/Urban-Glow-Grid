import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Get absolute file URL
        filepath = os.path.abspath("GenAI_Oral_Presentation.html")
        print(f"Generating PDF from: {filepath}")
        await page.goto(f"file://{filepath}")
        await page.emulate_media(media="print")
        # Generate PDF with A4 Landscape format
        await page.pdf(
            path="GenAI_Oral_Presentation.pdf", 
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        await browser.close()
        print("Success: GenAI_Oral_Presentation.pdf generated.")

if __name__ == "__main__":
    asyncio.run(main())
