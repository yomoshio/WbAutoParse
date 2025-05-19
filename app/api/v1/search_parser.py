import asyncio
from playwright.async_api import async_playwright
from urllib.parse import quote_plus


async def fetch_wb_page(page, url, page_num):
    print(f"🔄 Загружаем: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        # Подождём, пока появится элемент с товарами
        await page.wait_for_selector(".product-card__wrapper", timeout=10000)
        return await page.content()
    except Exception as e:
        print(f"❌ Ошибка при загрузке страницы {page_num}: {e}")
        return None



async def find_product_position(keyword: str, target_article: str, max_pages: int = 5):
    base_url = "https://www.wildberries.ru/catalog/0/search.aspx"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        position = 1
        for page_num in range(1, max_pages + 1):
            encoded_keyword = quote_plus(keyword)
            url = f"{base_url}?page={page_num}&sort=popular&search={encoded_keyword}"
            print(f"🔄 Загружаем: {url}")

            html = await fetch_wb_page(page, url, page_num)

            # 🕵️ Получаем список всех артикулов на странице
            items = await page.query_selector_all("article.product-card")
            print(f"📄 Страница {page_num}: найдено {len(items)} товаров")

            for idx, item in enumerate(items):
                nm_id = await item.get_attribute("data-nm-id")
                if nm_id == target_article:
                    await browser.close()
                    return position + idx

            position += len(items)

        await browser.close()
        return None


# 🚀 Запуск
if __name__ == "__main__":
    keyword = "точильный станок для ножей"
    target_article = "4356813"  # ← Артикул товара

    pos = asyncio.run(find_product_position(keyword, target_article))
    if pos:
        print(f"✅ Товар найден на позиции: {pos}")
    else:
        print("❌ Товар не найден в первых 5 страницах")
