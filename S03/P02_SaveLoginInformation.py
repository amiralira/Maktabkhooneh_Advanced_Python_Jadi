import mysql.connector
import re

# *************************************************************************************
# if you want to use this class please change your database credentials
db_credentials = {
    'host': '',  # default is localhost
    'port': 111,  # default is 3306
    'user': "",  # default is root
    'password': '****',
    'database': '****',
    'table_name': '****'}

# *************************************************************************************


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

# *************************************************************************************
# Check Email Format


def check_email_format(inp_email):
    # create pattern for correct email format: expression@string.string
    pattern = r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'

    # check if the input email matches the pattern
    if re.match(pattern, inp_email):
        return True
    else:
        return False

# *************************************************************************************
# Check password format


def check_password_format(inp_password):
    # create pattern for correct password format: only digits and characters
    pattern = r'^[a-zA-Z0-9]+$'

    # check if the input password matches the pattern
    if re.match(pattern, inp_password):
        return True
    else:
        return False

# *************************************************************************************
# Check duplicate email


def check_duplicate_email(email, info_dict):
    if email in info_dict:
        return True
    else:
        return False

# *************************************************************************************
# If you want to create a database and table, please uncomment the following lines
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
# 		username VARCHAR ( 255 ),
# 		password VARCHAR ( 255 ));""".format(db_credentials['table_name'])
#
# db_obj.cursor.execute(sql_query)
# db_obj.connection.commit()
# db_obj.cursor.close()

# *************************************************************************************
# select data
db_obj = Database(host=db_credentials['host'],
                  port=db_credentials['port'],
                  user=db_credentials['user'],
                  password=db_credentials['password'])

## use the database
sql_query = """USE {};""".format(db_credentials['database'])
db_obj.cursor.execute(sql_query)

sql_query = """SELECT * FROM {};""".format(db_credentials['table_name'])
db_obj.cursor.execute(sql_query)
result = db_obj.cursor.fetchall()
info_dict = {}
for row in result:
    info_dict[row[0]] = row[1]

# *************************************************************************************
# get email and password from user


email_address = input("Enter your email address: ")
Flag = False

while not Flag:
    if check_email_format(email_address):
        if check_duplicate_email(email_address, info_dict):
            print("This email is already registered, please enter another email address")
            email_address = input("Enter your email address: ")
        else:
            Flag = True
    else:
        print("Email format is not correct please try again with a correct format: expression@string.string")
        email_address = input("Enter your email address: ")

password = input("Enter your password: ")

Flag = False

while not Flag:
    if check_password_format(password):
        Flag = True
    else:
        print("Password format is not correct please try again with a correct format: only digits and characters")
        password = input("Enter your password: ")

# *************************************************************************************
# Insert Data
db_obj = Database(host=db_credentials['host'],
                  port=db_credentials['port'],
                  user=db_credentials['user'],
                  password=db_credentials['password'])

## use the database
sql_query = """USE {};""".format(db_credentials['database'])
db_obj.cursor.execute(sql_query)

sql_query = """INSERT INTO {} ( username, password )
VALUES
    ( '{}', '{}' );""".format(db_credentials['table_name'], email_address, password)


db_obj.cursor.execute(sql_query)
db_obj.connection.commit()
db_obj.cursor.close()


