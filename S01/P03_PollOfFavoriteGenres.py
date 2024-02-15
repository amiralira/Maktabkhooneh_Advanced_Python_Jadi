# get number of persons
number_of_persons = int(input())

base_list_of_genres = ["Horror", "Romance", "Comedy", "History", "Adventure", "Action"]

genres_list = []
genres_dict = dict()
# get the list of genres
genres = []
for i in range(number_of_persons):
    this = input().split()
    for genres in this[1:]:
        if genres in genres_dict:
            genres_dict[genres] += 1
        else:
            genres_dict[genres] = 1

for genre in base_list_of_genres:
    if genre not in genres_dict:
        genres_dict[genre] = 0


# convert the dictionary to a list of tuples
genres_list = list(genres_dict.items())

# sort the list of tuples first by the number of persons who like the genre and then by the genre name
genres_list.sort(key=lambda x: (-x[1], x[0]))

# print the list of genres with format "Action : 3"
for genre in genres_list:
    print(genre[0], ":", genre[1])
