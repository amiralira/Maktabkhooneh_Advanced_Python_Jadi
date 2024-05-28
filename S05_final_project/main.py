from bama_car_class import BamaCar
import asyncio


if __name__ == '__main__':
    first_index = 0

    list_of_indexes = [first_index + i for i in range(100)]

    list_of_objects = [BamaCar(page_index=index) for index in list_of_indexes]

    # get with gather
    async def start():
        await asyncio.create_task(BamaCar.get_proxies())
        smp = asyncio.Semaphore(5)
        result = await asyncio.gather(*[obj.main(smp=smp) for obj in list_of_objects], return_exceptions=True)
        print(result)
        return result

    res = asyncio.run(start())

    for item in res:
        print(item[0])
        item[1].to_excel('data.xlsx', index=False)
