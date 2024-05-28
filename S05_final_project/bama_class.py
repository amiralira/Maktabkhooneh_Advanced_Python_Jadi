import asyncio
import aiohttp


class Bama:

    def __init__(self,
                 page_index: int = 0):
        self.url = 'https://bama.ir/car'
        self.page_index = page_index
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.json_response = None

    async def fetch(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            return await response.json()

    async def request_data(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, self.url)
            return html

    async def get_data(self):
        this_json = await self.request_data()
        self.json_response = this_json
        print(self.json_response)

    async def parse_data(self):
        pass

    async def main(self,
                   smp: asyncio.Semaphore = 10):
        async with smp:
            # get data
            print(f'Getting data from {self.url}')
            await self.get_data()

        # parse data
        print(f'Parsing data from {self.url}')
        return await self.parse_data()




