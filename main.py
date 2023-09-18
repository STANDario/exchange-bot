import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys
import logging


async def request(url):
    async with aiohttp.ClientSession() as session:
        logging.info(f"Start with {url}")
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"End with {url}")
                    return result
                return
        except aiohttp.ClientConnectionError as e:
            return


async def get_exchange(count):

    result_for_all_days = []
    day = datetime.now().date()

    for _ in range(count):
        str_day = str(day).split("-")
        day_for_url = f"{str_day[2]}.{str_day[1]}.{str_day[0]}"
        result = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={day_for_url}")
        if result:
            valuta_for_day = {}
            exc = list(filter(lambda el: el["currency"] == "USD" or el["currency"] == "EUR", [i for i in result["exchangeRate"]]))

            for valuta in exc:
                valuta_for_day[valuta["currency"]] = {"sale": valuta["saleRate"], "purchase": valuta["purchaseRate"]}

            result_for_all_days.append({day_for_url: valuta_for_day})

        day = day - timedelta(days=1)

    return result_for_all_days


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s %(message)s',
        level=logging.INFO)

    while True:
        try:
            count = int(sys.argv[1])
            break
        except ValueError as e:
            print("Number of days must be a number!")
            quit()
        except IndexError as e:
            count = 1
            break

    if count == 0:
        print("Returns nothing :)")
        quit()
    elif count > 10:
        print("The maximum numbers of days is 10, please try again!")
        quit()
    elif count < 0:
        print("The number can`t be less than 0!")

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    x = asyncio.run(get_exchange(count))
    print(x)
