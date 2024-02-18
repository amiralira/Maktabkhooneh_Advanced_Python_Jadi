import re

inp_email = input()

# create pattern for correct email format: expression@string.string
pattern = r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'

# check if the input email matches the pattern
if re.match(pattern, inp_email):
    print('OK')
else:
    print('WRONG')
