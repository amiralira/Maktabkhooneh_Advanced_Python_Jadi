from bama_car_class import BamaCar
import asyncio
from database_class import DataBase
import pandas as pd
import random
from time import sleep


if __name__ == '__main__':
    first_index = 0

    while first_index < 900:
        list_of_indexes = [first_index + i for i in range(10)]
        first_index += 10

        list_of_objects = [BamaCar(page_index=index) for index in list_of_indexes]

        # get with gather
        async def start():
            await asyncio.create_task(BamaCar.get_proxies())
            smp = asyncio.Semaphore(5)
            result = await asyncio.gather(*[obj.main(smp=smp) for obj in list_of_objects], return_exceptions=True)
            return result

        res = asyncio.run(start())

        for item in res:
            # print(item[0])
            try:
                metadata_df = item[0]
                data_df = item[1]
                BamaCar.concat_data(data_df)
            except Exception as e:
                print(e)

        df = BamaCar.update_insert_change_data()

        BamaCar.df_all_results = pd.DataFrame()
        sleep_time = random.randint(10, 30)
        print(f'Sleeping for {sleep_time} seconds')
        sleep(sleep_time)


