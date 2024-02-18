import mysql.connector

# *************************************************************************************
# if you want to use this class please change your database credentials
db_credentials = {
    'host': '',  # default is localhost
    'port': 1111,  # default is 3306
    'user': "",  # default is root
    'password': '****',
    'database': 'DB_NAME',
    'table_name': 'TABLE_NAME'}
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


# # If you want to create a database and table and insert data, please uncomment the following lines
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
# 		Name VARCHAR ( 255 ),
# 		Weight INT,
# 		Height INT);""".format(db_credentials['table_name'])
#
# db_obj.cursor.execute(sql_query)
# db_obj.connection.commit()
# db_obj.cursor.close()
#
# # Insert Data
# db_obj = Database(host=db_credentials['host'],
#                   port=db_credentials['port'],
#                   user=db_credentials['user'],
#                   password=db_credentials['password'])
#
# ## use the database
# sql_query = """USE {};""".format(db_credentials['database'])
# db_obj.cursor.execute(sql_query)
#
# sql_query = """INSERT INTO {} ( NAME, Weight, Height )
# VALUES
# 	( 'Amin', 75, 180 ),
# 	( 'Mahdi', 90, 190 ),
# 	( 'Mohammad', 75, 175 ),
# 	( 'Ahmad', 60, 175 );""".format(db_credentials['table_name'])
#
# db_obj.cursor.execute(sql_query)
# db_obj.connection.commit()
# db_obj.cursor.close()


# Select Data
db_obj = Database(host=db_credentials['host'],
                  port=db_credentials['port'],
                  user=db_credentials['user'],
                  password=db_credentials['password'])

# # use the database
sql_query = """USE {};""".format(db_credentials['database'])

db_obj.cursor.execute(sql_query)

# get name of columns
sql_query = """SHOW COLUMNS FROM {};""".format(db_credentials['table_name'])
db_obj.cursor.execute(sql_query)
columns_result = db_obj.cursor.fetchall()
columns_name = [column[0] for column in columns_result]

sql_query = """SELECT * FROM {};""".format(db_credentials['table_name'])
db_obj.cursor.execute(sql_query)
result = db_obj.cursor.fetchall()

employee_dict = {}
for i, row in enumerate(result):
    employee_dict[i] = {columns_name[j]: row[j] for j in range(len(row))}

list_of_employee = []
for key, value in employee_dict.items():
    list_of_employee.append((value['Name'], value['Height'], value['Weight']))


# sort by height and weight
list_of_employee.sort(key=lambda x: (-x[1], x[2]))

# print the result with format: Name Height Weight
for employee in list_of_employee:
    print("{} {} {}".format(employee[0], employee[1], employee[2]))

