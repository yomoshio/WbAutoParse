import asyncio
from playwright.async_api import async_playwright


async def parse_wb_product(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()

        try:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_selector("h1.product-page__title", timeout=10000)
            title = await page.locator("h1.product-page__title").inner_text()
            await page.wait_for_selector("button.j-details-btn-desktop", timeout=10000)
            await page.click("button.j-details-btn-desktop")

            await page.wait_for_timeout(1000)


            await page.wait_for_selector("p.option__text", timeout=10000)
            description = await page.locator("p.option__text").inner_text()
            return title, description
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            await browser.close()


async def main(url: str):
    title, desc = await parse_wb_product(url)
    print(title, desc)


if __name__ == "__main__":
    asyncio.run(main("https://www.wildberries.ru/catalog/4356813/detail.aspx"))
