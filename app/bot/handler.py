from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from functools import partial

from app.parsers.parser import parse_wb_product
from app.bot.services.keyword import SearchKeywords
from app.api.v1.WB_stat import WB_stat
import aiohttp

router = Router()



class SearchStates(StatesGroup):
    waiting_for_url = State()



def setup_handlers(dp, chat_gpt):
    router.message.register(partial(cmd_search, chat_gpt=chat_gpt), Command("search"))
    router.message.register(partial(process_url, chat_gpt=chat_gpt), StateFilter(SearchStates.waiting_for_url))
    dp.include_router(router)



async def cmd_search(message: Message, state: FSMContext, chat_gpt):
    await state.set_state(SearchStates.waiting_for_url)
    await message.answer("🔗 Пожалуйста, отправьте ссылку на товар Wildberries.")



async def process_url(message: Message, state: FSMContext, chat_gpt):
    url = message.text.strip()
    await message.answer("🔍 Обрабатываю ссылку...")

    try:
        title, description = await parse_wb_product(url)
        await message.answer(f"📦 Название: {title}\n📝 Описание: {description[:200]}...")
    except Exception as e:
        await message.answer(f"❌ Не удалось получить данные товара: {e}")
        await state.clear()
        return

    async with aiohttp.ClientSession() as session:
        try:
            keyword_generator = SearchKeywords(chat_gpt=chat_gpt)
            keywords = await keyword_generator.generate_keywords(session=session, title=title, description=description)
        except Exception as e:
            await message.answer(f"❌ Ошибка генерации ключей: {e}")
            await state.clear()
            return

        stats = WB_stat()
        total_sum = 0
        results = []

        for kw in keywords:
            total = await stats.get_total(session, kw)
            total_sum += total
            results.append(f"{kw} — {total}")

    response = "\n".join(results[:20])
    await message.answer(f"📊 Ключевые слова и частотность:\n\n{response}\n\nОбщая сумма: {total_sum}")

    await state.clear()  
