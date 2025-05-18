import aiohttp
import json


class WB_stat:
    def __init__(self) -> None:
        self.headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "application/json, text/plain, */*"
                    }


    async def get_total(self, session: aiohttp.ClientSession, query: str):
        url = f'https://search.wb.ru/exactmatch/ru/male/v4/search?&appType=1&curr=rub&dest=-1181901&spp=27&query={query}&resultset=catalog&sort=popular&suppressSpellcheck=false&uclusters=8&ref=vc.ru'
        try:
            async with session.get(url, headers=self.headers) as response:
                text = await response.text()
                try:
                    data = json.loads(text)  
                    total = data.get("data", {}).get("total", 0)
                    return total
                except json.JSONDecodeError:
                    print(f"⚠️ Ошибка запроса {query}: не удалось разобрать JSON. Ответ: {text[:200]}")
                    total = 0
                    return total
        except Exception as e:
            print(f"❌ Ошибка запроса {query}: {e}")
            total = 0
            return total
