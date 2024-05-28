Text = input()

# split the sentences into
sentences = Text.split(".")

counter = 1
index_words = {}
for sentence in sentences:
    sentence = sentence.strip()
    words = sentence.split(" ")
    for i in range(0, len(words)):
        if i == 0:
            counter += 1
            continue
        if words[i][0].isupper():
            index_words[counter] = words[i].strip().replace(".", "").replace(",", "")
        counter += 1

list_of_words = []
for key, val in index_words.items():
    list_of_words.append((key, val))

list_of_words.sort(key=lambda x: x[0])

# print format: number:word
if len(list_of_words):
    for word in list_of_words:
        print("{}:{}".format(word[0], word[1]))
else:
    print("None")
