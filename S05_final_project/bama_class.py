import asyncio
import aiohttp
import pandas as pd
from queue import Queue


class Bama:
    proxies_queue = Queue(maxsize=10)

    def __init__(self,
                 page_index: int = 0):
        self.url = 'https://bama.ir/car'
        self.page_index = page_index
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.json_response = None

    async def fetch(self, session, url):
        proxy = self.proxies_queue.get()
        print(proxy)
        self.proxies_queue.put(proxy)
        async with session.get(url, headers=self.headers, proxy=proxy, ssl=False) as response:
            return await response.json()

    async def request_data(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, self.url)
            return html

    async def get_data(self):
        this_json = await self.request_data()
        self.json_response = this_json
        # print(self.json_response)
        # print("///////////////////////////////////////////////")

    async def parse_data(self):
        pass

    async def main(self,
                   smp: asyncio.Semaphore = 10):
        async with smp:
            # get data
            print(f'Getting data from {self.url}')
            await self.get_data()
            await asyncio.sleep(30)

        # parse data
        print(f'Parsing data from {self.url}')
        return await self.parse_data()

    @classmethod
    async def get_proxies(cls):
        if cls.proxies_queue.empty():
            print('Getting proxies')
            url = 'https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=10'
            headers = {"Authorization": "Token s6sqbv4bsexqa7aan5tbzcwm9nhcnaaozc29iudj"}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    proxies = await response.json()
                    all_proxies_result = proxies['results']
                    df = pd.json_normalize(all_proxies_result)
                    for index, row in df.iterrows():
                        # 'http://your_user:your_password@your_proxy_url:your_proxy_port'
                        this_proxy = f"http://{row['username']}:{row['password']}@{row['proxy_address']}:{row['port']}"
                        cls.proxies_queue.put(this_proxy)

            # shuffle proxies
            import random
            proxies_list = list(cls.proxies_queue.queue)
            random.shuffle(proxies_list)
            cls.proxies_queue.queue.clear()
            for proxy in proxies_list:
                cls.proxies_queue.put(proxy)




