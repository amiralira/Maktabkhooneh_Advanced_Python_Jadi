import asyncio
import aiohttp
import pandas as pd
from queue import Queue
from database_class import DataBase
from sqlalchemy import create_engine, text


class Bama:
    proxies_queue = Queue(maxsize=10)
    df_all_results = pd.DataFrame()

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
        # print(proxy)
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

    @classmethod
    def concat_data(cls, data_df):
        cls.df_all_results = pd.concat([cls.df_all_results, data_df], ignore_index=True)

    @classmethod
    def clean_data(cls):
        columns = ['type',
                   # 'images',
                   # 'banner',
                   # 'promotion',
                   # 'similarity',
                   'detail.type',
                   'detail.code',
                   # 'detail.rank',
                   # 'detail.badge',
                   # 'detail.pin',
                   'detail.url',
                   'detail.title',
                   'detail.subtitle',
                   'detail.trim',
                   'detail.time',
                   'detail.year',
                   'detail.mileage',
                   'detail.location',
                   'detail.specialcase',
                   'detail.transmission',
                   'detail.fuel',
                   'detail.color',
                   'detail.body_color',
                   'detail.inside_color',
                   'detail.body_status',
                   'detail.description',
                   'detail.authenticated',
                   'detail.body_type',
                   'detail.body_type_fa',
                   'detail.cylinder_fa',
                   # 'detail.image_count',
                   # 'detail.image',
                   'detail.modified_date',
                   'specs.volume',
                   'specs.engine',
                   'specs.acceleration',
                   'specs.fuel',
                   'specs.battery_capacity',
                   'specs.all_electric_range',
                   'specs.url_price',
                   'specs.url_review',
                   'dealer.id',
                   'dealer.type',
                   'dealer.package_type',
                   'dealer.name',
                   # 'dealer.logo',
                   'dealer.link',
                   'dealer.address',
                   'dealer.ad_count',
                   'dealer.score',
                   'price.type',
                   'price.price',
                   'price.prepayment',
                   'price.payment',
                   'price.prepayment_primary',
                   'price.prepayment_secondary',
                   'price.payment_primary',
                   'price.month_number',
                   'price.installments',
                   'price.delivery_days',
                   # 'metadata.title_tag',
                   # 'metadata.keywords',
                   # 'metadata.description',
                   # 'metadata.canonical',
                   # 'metadata.noindex',
                   # 'breadcrump.links',
                   # 'dealer',
                   # 'detail',
                   # 'specs',
                   # 'price',
                   # 'metadata',
                   # 'breadcrump',
                   # 'banner.type',
                   # 'banner.position',
                   # 'banner.title',
                   # 'banner.href',
                   # 'banner.aspect_ratio_desktop',
                   # 'banner.aspect_ratio_mobile',
                   # 'banner.mobile_large',
                   # 'banner.large_url']
                   ]
        cls.df_all_results = cls.df_all_results[columns].copy()

        # remove duplicates
        cls.df_all_results.drop_duplicates(inplace=True, keep='first')

        # remove rows with empty 'detail.code'
        cls.df_all_results.dropna(subset=['detail.code'], inplace=True)

        # remove rows with type 'banner'
        cls.df_all_results = cls.df_all_results[cls.df_all_results['type'] != 'banner'].copy()

    @classmethod
    def save_data(cls):
        # cls.df_all_results.to_excel('bama_cars.xlsx', index=False)
        db_object = DataBase()
        engin = db_object.engin
        with engin.connect() as con:
            cls.df_all_results.to_sql('bama_cars', con, if_exists='append', index=False, chunksize=1000)

    @classmethod
    def read_data_from_db(cls):
        db_object = DataBase()
        engin = db_object.engin
        with engin.connect() as con:
            df = pd.read_sql('bama_cars', con)
        return df

    @classmethod
    def update_insert_change_data(cls):
        try:
            df_perv_data = cls.read_data_from_db()
        except Exception as e:
            df_perv_data = pd.DataFrame()
        cls.clean_data()

        # merge two dataframes with right join on 'detail.code'
        if df_perv_data.empty:
            df = cls.df_all_results.copy()
        else:
            df = pd.merge(df_perv_data,
                          cls.df_all_results,
                          on='detail.code',
                          how='right',
                          suffixes=('_old', ''),
                          indicator=True)

            df = df[df['_merge'] == 'right_only'].copy()
            df.drop(columns='_merge', inplace=True)



        # delete old data
        cols = [col for col in df.columns if col.endswith('_old')]
        df.drop(columns=cols, inplace=True)

        # delete rows from database with 'detail.code' in df
        delete_detail_code = df['detail.code'].tolist()
        query = f"DELETE FROM bama_cars WHERE `detail.code` IN {tuple(delete_detail_code)}"

        if str(query).endswith(',)'):
            query = str(query)[:-2] + ')'

        db_object = DataBase()
        engin = db_object.engin
        with engin.connect() as con:
            try:
                con.execute(text(query))
            except Exception as e:
                print(e)

        # insert new data
        cls.df_all_results = df.copy()
        cls.save_data()

