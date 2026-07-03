import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    html_path = "/Users/Abir/Desktop/innovation project/presentation_slide.html"
    screenshot1_path = "/Users/Abir/Desktop/innovation project/tech_slide1.png"
    screenshot3_path = "/Users/Abir/Desktop/innovation project/tech_slide3.png"
    screenshot5_path = "/Users/Abir/Desktop/innovation project/tech_slide5.png"
    screenshot6_path = "/Users/Abir/Desktop/innovation project/tech_slide6.png"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1414, "height": 1000})
        filepath = os.path.abspath(html_path)
        await page.goto(f"file://{filepath}")
        await page.wait_for_timeout(1000)
        
        slide1 = await page.query_selector("#slide1")
        if slide1:
            await slide1.screenshot(path=screenshot1_path)
            print("Captured Slide 1")
            
        slide3 = await page.query_selector("#slide3")
        if slide3:
            await slide3.screenshot(path=screenshot3_path)
            print("Captured Slide 3")
            
        slide5 = await page.query_selector("#slide5")
        if slide5:
            await slide5.screenshot(path=screenshot5_path)
            print("Captured Slide 5")
            
        slide6 = await page.query_selector("#slide6")
        if slide6:
            await slide6.screenshot(path=screenshot6_path)
            print("Captured Slide 6")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
