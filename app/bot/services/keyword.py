from typing import List, Tuple
import aiohttp
import asyncio
from aiocache import Cache, cached
from aiohttp import ClientTimeout



class SearchKeywords:
    def __init__(self, chat_gpt):
        self.chat_gpt = chat_gpt
        self.timeout = ClientTimeout(total=10)


    async def generate_keywords(self, session: aiohttp.ClientSession, title: str, description: str) -> List[str]:
        description = description or "Описание отсутствует."
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты опытный SEO-специалист. Твоя задача — по названию и описанию товара составить список из 10 релевантных поисковых ключевых фраз для Wildberries.\n"
                    "Мысли как покупатель: через какие слова и фразы он будет искать этот товар?\n"
                    "Учитывай название, характеристики, назначение и целевую аудиторию.\n"
                    "Формат ответа: список из 10 ключевых фраз, каждая — на новой строке, без номеров и лишних символов.\n"
                    "Не пиши ничего, кроме самих ключевых фраз."
                )
            },
            {
                "role": "user",
                "content": f"Название: {title}\nОписание: {description}"
            }
        ]

        for attempt in range(3):
            try:
                res = await self.chat_gpt.ask(
                    session=session,
                    messages=messages,
                    model="gpt-4.1-nano",
                    timeout=self.timeout
                )
                raw_keywords = res["choices"][0]["message"]["content"].strip().split("\n")
                keywords = [kw.strip() for kw in raw_keywords if kw.strip()]
                print(f"🔧 Сгенерированы ключевые слова для '{title}': {keywords}... (всего {len(keywords)})")
                return keywords
            except asyncio.TimeoutError:
                print(f"⏳ Таймаут в generate_keywords для '{title}' (попытка {attempt + 1}/3)")
                if attempt < 2:
                    await asyncio.sleep(1)
                else:
                    print(f"❌ Все попытки исчерпаны для '{title}', возвращаю пустой список")
                    return []
            except Exception as e:
                print(f"❌ Ошибка в generate_keywords для '{title}': {e}")
                return []
