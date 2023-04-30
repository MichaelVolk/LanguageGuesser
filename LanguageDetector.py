import random


import tensorflow as tf
import numpy
import config as con
import sklearn


max_letters = con.max_letters  # max amount of letters per word
words_per_language = con.words_per_language  # how many words per language are used to train
num_letters = con.num_letters  # amount of different letters in alphabet (123 for all european languages)
listoflangs = ["afr", "bos", "cze", "dan", "dut", "eng", "est", "fin", "fre", "ger", "hrv", "hun", "ice",
               "ita", "lav", "lit", "nor", "pol", "por", "slk", "slv", "spa", "srp",  "swe", "ukr"]
# Ask user to select the languages he wants the model to learn.
user_select = True
langs = []
while user_select:
    print("You can select the following languages: ", listoflangs)
    selected_lang = input("Please enter language. Enter 'done' when done. Type 'all' to add all Languages. ")
    if selected_lang == "done":
        user_select = False
    elif selected_lang == "all":
        langs = listoflangs
        user_select = False
    elif selected_lang not in listoflangs:
        print("Language not found or already selected.")
    else:
        listoflangs.remove(selected_lang)
        langs.append(selected_lang)
        if len(langs) >= 10:
            print("Maximum of 10 languages reached!")
            user_select = False
            break
nTrain = len(langs)*words_per_language  # total length of training data
# creating a dict to associate each language with an integer
langdict = {}
for lang in langs:
    langdict[langs.index(lang)] = lang

words_train = []
words_test = []
index_train = []
index_test = []
# for each language, read the word list file
# then shuffle and select words for test and train data
print("reading text files...")
for lang in langs:
    lang_file = "data/"+lang+"_large.txt"
    word_list = []  # temp list storing the words from the language
    index_list = []  # temp list storing the index of the language for every word
    with open(lang_file, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            word_list.append(line[0:max_letters].strip().lower())
            index_list.append(langs.index(lang))
    random.shuffle(word_list)
    words_train = words_train + word_list[0:words_per_language]
    index_train = index_train + index_list[0:words_per_language]
    words_test = words_test + word_list[words_per_language:2*words_per_language]
    index_test = index_test + index_list[words_per_language:2*words_per_language]
words_train, index_train = sklearn.utils.shuffle(words_train, index_train)
words_test, index_test = sklearn.utils.shuffle(words_test, index_test)
# setting up the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(200, input_dim=num_letters * max_letters, activation='sigmoid'))
model.add(tf.keras.layers.Dense(450, activation='sigmoid'))
model.add(tf.keras.layers.Dense(150, activation='sigmoid'))
model.add(tf.keras.layers.Dense(len(langs), activation='softmax'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
# prepare solution vectors for training data. Target values are in [0.01,0.99] instead of [0,1] to prevent large weights
# since the sigmoid function can't actually reach the values 0 and 1
print("preparing training data...")
y_train = []
for i in range(len(words_train)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(index_train[i])] = 0.99
    y_train.append(soli)
# prepare training data: take each word and convert them into a vector
x_train = []
for i in range(nTrain):
    word = words_train[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1))
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.get_index_of_letter(c)] = 1
    x_train.append(wordlist)
x_train = numpy.array(x_train)
y_train = numpy.array(y_train[0:nTrain])
x_train = x_train[:, :, 0]  # these two steps are necessary because numpy sees the data as 3-dim array
y_train = y_train[:, :, 0]
# As above, create solution vectors, this time for test data
print("preparing test data...")
y_test = []
for i in range(len(words_test)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(index_test[i])] = 0.99
    y_test.append(soli)
x_test = []
# convert test data to input vectors
for i in range(nTrain):
    word = words_test[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1))
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.get_index_of_letter(c)] = 1
    x_test.append(wordlist)
x_test = numpy.array(x_test)
y_test = numpy.array(y_test[0:nTrain])
x_test = x_test[:, :, 0]
y_test = y_test[:, :, 0]
# train and test the model
model.fit(x_train, y_train, epochs=con.eps)
x = model.evaluate(x_test, y_test)
print(x)
while True:
    input_word = input("Please enter a word:")
    if input_word.isnumeric():
        input_num = int(input_word)
        print(words_test[input_num])
        print(index_test[input_num])
        print(langdict[index_test[input_num]])
        print("---")
        print(words_train[input_num])
        print(index_train[input_num])
        print(langdict[index_train[input_num]])
    else:
        query_word = [con.get_word_vector(input_word)]
        qw = numpy.array(query_word)
        qw = qw[:, :, 0]
        pred_vect = model.predict(qw)
        max_val = numpy.max(pred_vect)
        print(numpy.argmax(pred_vect))
        # the next line is used to suppress a warning about type mismatch in line 113 (int vs ndarray[int])
        # noinspection PyTypeChecker
        max_lang = langdict[numpy.argmax(pred_vect)]
        print("I am ", max_val*100, "% certain ", input_word, " is ", max_lang)
        print(pred_vect)
