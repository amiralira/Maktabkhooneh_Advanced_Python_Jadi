import random

import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import re
import json
from tqdm import tqdm
from colorama import Fore
import sqlalchemy
from urllib.parse import quote_plus
import mysql.connector

# if you want to use this class please change your database credentials
db_credentials = {
    'host': 'localhost',  # default is localhost
    'port': 3306,  # default is 3306
    'user': "root",  # default is root
    'password': 'Amirali-55662282',
    'database': 'truecar_db',
    'table_name': 'used_car'}


class TrueCar:
    flag_get_input = False
    make = None
    model = None
    year = None
    base_url = 'https://www.truecar.com/used-cars-for-sale/listings/'
    full_base_url = ''
    last_page = 0

    def __init__(self,
                 page=1):

        self.page = page
        self.full_url_with_page = ''
        self.page_content = None

        if not self.flag_get_input:
            TrueCar.get_make()
            TrueCar.get_model()
            TrueCar.get_year()
            TrueCar.create_full_base_url()
            TrueCar.flag_get_input = True

        self.create_full_url_with_page()

    @staticmethod
    def get_make():
        # get the make list format aaaa bbbb cccc if want all enter all
        str_make = input('Enter the make in format aaaa bbbb cccc or all (make_ex:: toyota bmw): ')
        if str_make == 'all':
            TrueCar.make = None
        else:
            TrueCar.make = str_make.split()

    @staticmethod
    def get_model():
        # get the model list format aaaa bbbb cccc if want all enter all
        str_model = input('Enter the model in format aaaa bbbb cccc or all (model_ex:: bmw_7-series toyota_camry): ')
        if str_model == 'all':
            TrueCar.model = None
            return
        else:
            TrueCar.model = str_model.split()

        # all to lower case
        TrueCar.model = [model.lower() for model in TrueCar.model]

    @staticmethod
    def get_year():
        # get min and max year
        min_year = input('Enter the min year or enter (no) for no min year: ')
        max_year = input('Enter the max year or enter (no) for no max year: ')
        if min_year == 'no':
            min_year = 'min'
        if max_year == 'no':
            max_year = 'max'

        # year-2019-max
        if (min_year == 'min') and (max_year == 'max'):
            TrueCar.year = None
        else:
            TrueCar.year = f'year-{min_year}-{max_year}'

    @staticmethod
    def create_full_base_url():
        # https://www.truecar.com/used-cars-for-sale/listings/year-min-2013/?mmt[]=bmw_1-series&mmt[]=toyota_4runner
        TrueCar.full_base_url = TrueCar.base_url
        if TrueCar.year:
            TrueCar.full_base_url += f'{TrueCar.year}/'

        TrueCar.full_base_url += '?'
        if TrueCar.model:
            for model in TrueCar.model:
                TrueCar.full_base_url += f'mmt[]={model}&'
        else:
            if TrueCar.make:
                for make in TrueCar.make:
                    TrueCar.full_base_url += f'mmt[]={make}&'

        TrueCar.full_base_url = TrueCar.full_base_url[:-1]
        # print("full_base_url: ", TrueCar.full_base_url)

    def create_full_url_with_page(self):
        self.full_url_with_page = f'{self.full_base_url}&page={self.page}'

    # "https://www.truecar.com/used-cars-for-sale/listings/year-2018-2022/?mmt[]=bmw_7-series&mmt[]=toyota_camry&page=15"
    # "https://www.truecar.com/used-cars-for-sale/listings/year-2018-2022/?mmt[]=bmw_7-series&mmt[]=toyota_camry&page=2"


    def request_to_page(self):
        # request to page
        url_with_page = f'{self.full_base_url}?&page={self.page}'
        counter = 0
        max_counter = 5
        while counter < max_counter:
            try:
                self.page_content = requests.get(url_with_page)
                return self, True
            except Exception as e:
                print(e)
                counter += 1
                continue
        return self, False

    def get_last_page(self):
        soup = BeautifulSoup(self.page_content.text, 'html.parser')

        # get last page
        last_page_tag = (soup.find_all('li', {'class': 'hidden-sm-down page-item', 'data-test': 'paginationItem'}))[-1]
        # print(last_page_tag)
        last_page = int(last_page_tag.text)
        # print("last_page: ", last_page)
        TrueCar.last_page = last_page

    def parse_page(self) -> pd.DataFrame:
        all_res_df = pd.DataFrame()
        # parse page
        soup = BeautifulSoup(self.page_content.text, 'html5lib')
        # print(soup)
        base_cars_tag = soup.find('ul', {'class': 'row mb-3 mt-1'})
        car_tags_1 = base_cars_tag.find_all('li', {'class': 'mt-2 flex grow col-md-6 col-xl-4'})
        car_tags_2 = base_cars_tag.find_all('li', {'class': 'mt-3 flex grow col-md-6 col-xl-4'})
        # car_tags_0 = base_cars_tag.find_all('li')
        all_cars_tags = car_tags_1 + car_tags_2
        for car_tag in all_cars_tags:
            # class relative rounded-md shadow-lg
            label = ""
            data_test = ""
            data_test_dealerid = ""
            data_test_item = ""
            relative_tag = car_tag.find('div', {'class': 'relative rounded-md shadow-lg'})
            label = str(relative_tag.get('aria-label')).replace('View details for ', '')
            # print("label: ", label)
            data_test = relative_tag.get('data-test')
            # print("data_test: ", data_test)
            data_test_dealerid = relative_tag.get('data-test-dealerid')
            # print("data_test_dealerid: ", data_test_dealerid)
            data_test_item = relative_tag.get('data-test-item')
            # print("data_test_item: ", data_test_item)

            # get w-full truncate info
            w_full_tag = car_tag.find('div', {'class': 'w-full truncate'})

            # info of vehicleCardInfo
            vehicle_card_info_tag = w_full_tag.find('div', {'data-test': 'vehicleCardInfo'})

            # data test vehicleCardConditionYearMake
            data_test_vehicle_card_condition_year_make = vehicle_card_info_tag.find('div', {
                'data-test': 'vehicleCardConditionYearMake'})
            # print("data_test_vehicle_card_condition_year_make: ", data_test_vehicle_card_condition_year_make.text)

            # split the data_test_vehicle_card_condition_year_make with regex \s
            data_test_vehicle_card_condition_year_make_list = re.split(r'\s', data_test_vehicle_card_condition_year_make.text)
            # print("data_test_vehicle_card_condition_year_make_list: ", data_test_vehicle_card_condition_year_make_list)
            data_test_vehicle_card_condition_year_make_list = json.dumps(data_test_vehicle_card_condition_year_make_list)

            # data test vehicleCardTrim
            data_test_vehicle_card_trim = vehicle_card_info_tag.find('div', {'data-test': 'vehicleCardTrim'})

            # split the data_test_vehicle_card_trim with regex \s
            data_test_vehicle_card_trim_list = re.split(r'\s', data_test_vehicle_card_trim.text)
            data_test_vehicle_card_trim_list = json.dumps(data_test_vehicle_card_trim_list)
            # print("data_test_vehicle_card_trim_list: ", data_test_vehicle_card_trim_list)

            # price and mileage
            price = None
            excellent_price_label = None
            unit = None
            mileage = None

            price_mileage_tag = w_full_tag.find('div', {'class': 'mt-1 flex items-center justify-between'})

            # price
            price_tag = price_mileage_tag.find('h3')
            price = price_tag.text
            price = price.replace('$', '').replace(',', '')
            try:
                price = float(price)
            except:
                price = None
            # print("price: ", price)

            # excellent_price_label
            excellent_price_label = None
            excellent_price_label_tag = price_mileage_tag.find('div', {'data-test': 'vehicleCardPriceRating'})
            if excellent_price_label_tag:
                excellent_price_label = excellent_price_label_tag.text
            # print("excellent_price_label: ", excellent_price_label)

            # mileage and unit
            mileage = None
            unit = None
            mileage_tag = price_mileage_tag.find('div', {'data-test': 'vehicleMileage'})

            if mileage_tag:
                mileage_unit_text = mileage_tag.text
                mileage, unit = re.split(r'\s', mileage_unit_text)

                if "k" in mileage:
                    mileage = mileage.replace("k", "")
                    mileage = float(mileage) * 1000
                elif "m" in mileage:
                    mileage = mileage.replace("m", "")
                    mileage = float(mileage) * 1000000
                else:
                    mileage = float(mileage)

                if unit == 'mi':
                    unit = 'miles'
                elif unit == 'km':
                    unit = 'kilometers'

                # print("mileage: ", mileage)
                # print("unit: ", unit)

            # city and state
            # Palmetto Bay, FL
            city = None
            state = None
            city_state_tag = car_tag.find('div', {'data-test': 'vehicleCardFooter'})

            city, state = re.split(r',', city_state_tag.text)
            city = city.strip()
            state = state.strip()
            # print("city: ", city)
            # print("state: ", state)


            res_dict = {
                'label': label,
                'data_test': data_test,
                'data_test_dealerid': data_test_dealerid,
                'data_test_item': data_test_item,
                'data_test_vehicle_card_condition_year_make_list': data_test_vehicle_card_condition_year_make_list,
                'data_test_vehicle_card_trim_list': data_test_vehicle_card_trim_list,
                'price': price,
                'excellent_price_label': excellent_price_label,
                'mileage': mileage,
                'unit': unit,
                'city': city,
                'state': state
            }

            # print("res_dict: ", res_dict)
            res_df = pd.DataFrame(res_dict, index=[0])
            all_res_df = pd.concat([all_res_df, res_df], ignore_index=True)

            # print("*" * 100)

        return all_res_df


if __name__ == '__main__':

    # create database if not exists
    user = quote_plus(db_credentials['user'])
    password = quote_plus(db_credentials['password'])
    host = db_credentials['host']
    database = db_credentials['database']

    query = f"CREATE DATABASE IF NOT EXISTS {database};"
    conn = mysql.connector.connect(user=user, password=password, host=host)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

    temp_tc = TrueCar()
    max_workers = 50
    # tc.request_to_page(2)

    # get last page
    temp_tc.request_to_page()
    temp_tc.get_last_page()

    list_of_urls_with_pages = [TrueCar(page=i) for i in range(1, TrueCar.last_page + 1)]
    output_list = []

    # list_of_urls_with_pages = list_of_urls_with_pages[:10].copy()
    if len(list_of_urls_with_pages) > max_workers:
        req_list = random.sample(list_of_urls_with_pages, max_workers)
    else:
        req_list = list_of_urls_with_pages.copy()

    print(Fore.YELLOW + "Its taking time to get the data, because we are scraping all the pages :))), please wait...")
    while len(list_of_urls_with_pages) > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = (executor.submit(i.request_to_page) for i in req_list)
            for future in as_completed(future_to_url):
                try:
                    if future.result()[1]:
                        output_list.append(future.result()[0])
                    list_of_urls_with_pages.remove(future.result()[0])
                except Exception as exc:
                    continue
        if len(list_of_urls_with_pages) > max_workers:
            req_list = random.sample(list_of_urls_with_pages, max_workers)
        else:
            req_list = list_of_urls_with_pages.copy()

    all_get_data_df = pd.DataFrame()

    for output in tqdm(output_list, desc=Fore.GREEN + "Parsing pages"):
        # print(output.full_url_with_page)
        this_df = output.parse_page()
        all_get_data_df = pd.concat([all_get_data_df, this_df], ignore_index=True)

    # clean the data
    # # change order of columns
    columns = ['data_test_item',
               'label',
               'price',
               'mileage',
               'unit',
               'city',
               'state',
               'data_test_dealerid',
               'data_test_vehicle_card_condition_year_make_list',
               'data_test_vehicle_card_trim_list',
               'excellent_price_label',
               'data_test']

    all_get_data_df = all_get_data_df[columns]

    # # sort the data by data_test_item, label, price, mileage, city, state
    all_get_data_df.sort_values(by=['data_test_item', 'label', 'price', 'mileage', 'city', 'state'], inplace=True)

    # # drop duplicates
    all_get_data_df.drop_duplicates(inplace=True)

    # get the data from db
    user = quote_plus(db_credentials['user'])
    password = quote_plus(db_credentials['password'])
    host = db_credentials['host']
    database = db_credentials['database']
    table_name = db_credentials['table_name']

    query = f"SELECT * FROM {table_name};"
    try:
        db_df = pd.read_sql(query, f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    except:
        db_df = pd.DataFrame()

    # find new data
    if len(db_df) == 0:
        new_data = all_get_data_df.copy()
    else:
        new_data = pd.merge(left=all_get_data_df,
                            right=db_df,
                            how='outer',
                            indicator=True)
        new_data = new_data[new_data['_merge'] == 'left_only']
        new_data.drop(columns='_merge', inplace=True)
    print(Fore.BLUE + "count of new data: ", new_data.shape[0])

    # # expired data
    # expired_data = pd.merge(left=all_get_data_df,
    #                         right=db_df,
    #                         how='outer',
    #                         indicator=True)
    # expired_data = expired_data[expired_data['_merge'] == 'right_only']
    # expired_data.drop(columns='_merge', inplace=True)

    # insert the new data to db
    user = quote_plus(db_credentials['user'])
    password = quote_plus(db_credentials['password'])
    host = db_credentials['host']
    database = db_credentials['database']
    table_name = db_credentials['table_name']

    engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    new_data.to_sql(table_name, con=engine, if_exists='replace', index=False)



