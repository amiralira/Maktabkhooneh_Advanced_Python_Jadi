# get number of lines

num_lines = int(input())

english_dict = {}
france_dict = {}
german_dict = {}

for i in range(num_lines):
    line = input().split()
    english_dict[line[1]] = line[0]
    france_dict[line[2]] = line[0]
    german_dict[line[3]] = line[0]

text = input().split()
translate_text = []

for word in text:
    if word in english_dict:
        translate_text.append(english_dict[word])
    elif word in france_dict:
        translate_text.append(france_dict[word])
    elif word in german_dict:
        translate_text.append(german_dict[word])
    else:
        translate_text.append(word)

print(' '.join(translate_text))
