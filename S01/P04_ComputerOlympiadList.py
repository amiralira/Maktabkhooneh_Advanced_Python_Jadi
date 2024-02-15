number_of_persons = int(input())
dict_of_persons = dict()
for i in range(number_of_persons):
    this = input().split(".")
    # start name with uppercase
    name_of_person = this[1].strip().capitalize()
    sex_of_person = this[0].strip()
    language_of_person = this[2].strip()
    dict_of_persons[name_of_person] = {"sex": sex_of_person,
                                       "language": language_of_person}

result_list = []
for key, value in dict_of_persons.items():
    result_list.append((value["sex"], key, value["language"]))

# sort first by sex and then by name
result_list.sort(key=lambda x: (x[0], x[1]))

# print with format "f Mina C":
for result in result_list:
    print(result[0], result[1], result[2])

