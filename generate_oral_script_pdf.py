import asyncio
from playwright.async_api import async_playwright
import os

async def generate_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_path = f"file://{os.path.abspath('oral_script.html')}"
        await page.goto(file_path, wait_until="networkidle")
        await page.pdf(path="team22_Oral_Script.pdf", format="A4", print_background=True)
        await browser.close()
        print("✅ team22_Oral_Script.pdf generated successfully.")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
