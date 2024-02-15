import datetime

# get date with format YYYY/MM/DD

birth_date = input()
try:
    birth_date = datetime.datetime.strptime(birth_date, '%Y/%m/%d')
    current_date = datetime.datetime.now()
    # convert to seconds
    age = current_date - birth_date
    age = age.total_seconds()
    # convert to years
    age = age / (60 * 60 * 24 * 365)
    print(int(age))
except Exception as e:
    print("WRONG")