import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import mysql.connector
import json


class Divar:
    result_list = []
    tavafoqi_list = []
    def __init__(self,
                 inp_city='tehran',
                 inp_page_number=1):
        self.city = inp_city
        self.page_number = inp_page_number
        self.pure_url = 'https://divar.ir'
        self.base_url = 'https://divar.ir/s/{}?page={}'.format(self.city, self.page_number)
        self.html_response = None
        self.result_list = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def get_page(self):
        try:
            r = requests.get(self.base_url, headers=self.headers)
            if r.status_code == 200:
                self.html_response = r.text
            else:
                print('Error in get_page: status_code is not 200')

        except Exception as e:
            print('Error in get_page: ', e)
            # print('url: ', self.base_url)

    def parse_page(self):
        inp_soup = None
        try:
            inp_soup = BeautifulSoup(self.html_response, 'html.parser')
        except Exception as e:
            print('Error in parse_page: ', e)

        if inp_soup is None:
            print('Error in parse_page: inp_soup is None')
            return

        # find all the notices
        notices_base_tags = inp_soup.find_all('div', class_='post-list__widget-col-c1444')

        # find information of each notice
        for notice in notices_base_tags:
            this_dict = {}

            # title
            title = notice.find('h2', class_='kt-post-card__title').text
            # print('title: ', title)

            # descriptions
            descriptions_list = []
            description_tags = notice.find_all('div', class_='kt-post-card__description')
            if len(description_tags) > 0:
                for description_tag in description_tags:
                    this_description = str(description_tag.text).strip()
                    descriptions_list.append(this_description)
            # print('descriptions: ', descriptions_list)

            # bottom part
            bottom_parts = []
            bottom_part = notice.find('div', class_='kt-post-card__bottom')
            if bottom_part:
                all_bottom_parts = bottom_part.find_all('span')
                for this_bottom_part in all_bottom_parts:
                    this_text = str(this_bottom_part.text).strip()
                    bottom_parts.append(this_text)
            # print('bottom_parts: ', bottom_parts)

            # url
            url = ""
            notice_url = notice.find('a').get('href')
            if notice_url:
                url = self.pure_url + notice_url
            # print('url: ', url)

            this_dict['title'] = title
            this_dict['description'] = descriptions_list
            this_dict['bottom_parts'] = bottom_parts
            this_dict['url'] = url
            self.result_list.append(this_dict)

        Divar.result_list = Divar.result_list + self.result_list

    @classmethod
    def check_tavafoqi(cls):
        flag = False
        for item in cls.result_list:
            for desc in item['description']:
                if 'توافقی' in desc:
                    cls.tavafoqi_list.append(item)
                    flag = True
        if flag:
            return True
        else:
            return False


class Database:
    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='root',
                 password='root'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def get_cursor(self):
        return self.connection.cursor()

# this code get notices from divar.ir and check if there is any tavafoqi notice
# if there is any tavafoqi notice it will print the information of the notice
# if first page does not have any tavafoqi notice it will go to the next page and check again
# it will continue until it finds a tavafoqi notice or it reaches the max_count default is first 10 pages
# if you want to change the city you can change the city variable


if __name__ == '__main__':

    city = 'tehran'
    # if want to change the city uncomment the following line
    # city = input('Enter the city: ')
    # *************************************************************************************

    # if you want to save data in a database uncomment the following lines and change the credentials and uncomment the
    # lines 196 to 247
    db_credentials = {
        'host': '',  # default is localhost
        'port': 111,  # default is 3306
        'user': "",  # default is root
        'password': '****',
        'database': '****',
        'table_name': '****'}

    flag_tavafoqi = False
    max_count = 10
    page_number = 1
    while (not flag_tavafoqi) and (page_number <= max_count):
        print('page_number: ', page_number)
        divar = Divar(city, page_number)
        divar.get_page()
        divar.parse_page()
        # print(len(Divar.result_list))
        if Divar.check_tavafoqi():
            flag_tavafoqi = True
            # print(Divar.tavafoqi_list)
        else:
            page_number += 1
            sleep(3)

    if flag_tavafoqi:
        # print the tavafoqi notices
        for item in Divar.tavafoqi_list:
            print('-----------------------------')
            print('title: ', item['title'])
            print('description: ', item['description'])
            print('bottom_parts: ', item['bottom_parts'])
            print('url: ', item['url'])

        # # save the tavafoqi notices in a csv file
        # with open('tavafoqi_notices.csv', 'w', encoding="utf-8") as f:
        #     # write the header
        #     f.write('title,description,bottom_parts,url\n')
        #     for item in Divar.tavafoqi_list:
        #         title = item['title']
        #         description = item['description']
        #         bottom_parts = item['bottom_parts']
        #         url = item['url']
        #         f.write('{},{},{},{}\n'.format(title, description, bottom_parts, url))

        # # save the tavafoqi notices in a database
        # # If you want to create a database and table, please uncomment the following lines
        # # create Database
        # db_obj = Database(host=db_credentials['host'],
        #                   port=db_credentials['port'],
        #                   user=db_credentials['user'],
        #                   password=db_credentials['password'])
        #
        # sql_query = """CREATE DATABASE IF NOT EXISTS {};""".format(db_credentials['database'])
        # db_obj.cursor.execute(sql_query)
        # db_obj.connection.commit()
        # db_obj.cursor.close()
        #
        # # create Table
        # db_obj = Database(host=db_credentials['host'],
        #                   port=db_credentials['port'],
        #                   user=db_credentials['user'],
        #                   password=db_credentials['password'])
        # ## use the database
        # sql_query = """USE {};""".format(db_credentials['database'])
        # db_obj.cursor.execute(sql_query)
        #
        # sql_query = """CREATE TABLE
        # IF
        # 	NOT EXISTS {} (
        # 		title VARCHAR ( 255 ),
        # 		description VARCHAR ( 255 ),
        #       bottom_parts VARCHAR ( 255 ),
        #       url VARCHAR ( 255 )
        # 		);""".format(db_credentials['table_name'])
        #
        # db_obj.cursor.execute(sql_query)
        # db_obj.connection.commit()
        # db_obj.cursor.close()
        #
        # # insert data
        # db_obj = Database(host=db_credentials['host'],
        #                   port=db_credentials['port'],
        #                   user=db_credentials['user'],
        #                   password=db_credentials['password'])
        # ## use the database
        # sql_query = """USE {};""".format(db_credentials['database'])
        # db_obj.cursor.execute(sql_query)
        #
        # for item in Divar.tavafoqi_list:
        #     title = item['title']
        #     description = str(item['description']).replace("'", "")
        #     bottom_parts = str(item['bottom_parts']).replace("'", "")
        #     url = item['url']
        #     sql_query = """INSERT INTO {} (title, description, bottom_parts, url) VALUES ('{}', '{}', '{}', '{}');""".format(db_credentials['table_name'], title, description, bottom_parts, url)
        #     db_obj.cursor.execute(sql_query)
        #     db_obj.connection.commit()

        # *************************************************************************************

    else:
        print('No tavafoqi notice found in first {} pages'.format(max_count))








