import aiohttp


class OpenAIApi:
    def __init__(self, key: str, proxy: str) -> None:
        self.key = key
        self.headers = {
            'Authorization': 'Bearer ' + key
        }
        self.proxy = proxy

    async def ask(self, session: aiohttp.ClientSession, messages: list[dict], model: str, timeout):
        url = 'https://api.openai.com/v1/chat/completions'
        data = {
            'model': model,
            'messages': messages
        }
        response = await session.post(url=url, json=data, headers=self.headers, proxy=self.proxy, timeout=timeout)
        if response.status != 200:
            raise Exception(f'Не удалось получить ответ ChatGTP! ({response.status})\n{await response.text()}')
        result = await response.json()
        return result
