import random
import tensorflow as tf
import numpy
import config as con

max_letters = con.max_letters  # max amount of letters per word
words_per_language = con.words_per_language  # how many words per language are used to train
num_letters = con.num_letters  # amount of different letters in alphabet (123 for all european languages)
listoflangs = ["bos", "cze", "dan", "dut", "eng", "fin", "fre", "ger", "hrv", "hun", "ice",
               "ita", "nor", "pol", "por", "slk", "slv", "spa", "srp",  "swe", "ukr"]
# Ask user to select the languages he wants the model to learn.
user_select = True
langs = []
while user_select:
    print("You can select the following languages: ", listoflangs)
    selected_lang = input("Please enter language. Enter 'done' when done")
    if selected_lang == "done":
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
print(langdict)
wordstrain = []
wordstest = []
# for each language, read the word list file, and at the index of the language to the end of each word
# then shuffle and select words for test and train data
for lang in langs:
    langfile = "data/"+lang+"_large.txt"
    langlist = []
    with open(langfile, 'r') as file:
        for line in file.readlines():
            langlist.append(line[0:max_letters].strip().lower() + str(langs.index(lang)))
    random.shuffle(langlist)
    wordstrain = wordstrain + langlist[0:words_per_language]
    wordstest = wordstest + langlist[words_per_language:2*words_per_language]
random.shuffle(wordstrain)
random.shuffle(wordstest)
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
# the index added to each word in the last step is also removed
sol = []
for i in range(len(wordstrain)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(wordstrain[i][-1])] = 0.99
    sol.append(soli)
    wordstrain[i] = wordstrain[i][:-1]
# prepare training data: take each word and convert them into a vector
inputs = []
for i in range(nTrain):
    word = wordstrain[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1))
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.getnumber(c)] = 1
    inputs.append(wordlist)
x_train = numpy.array(inputs)
y_train = numpy.array(sol[0:nTrain])
x_train = x_train[:, :, 0]  # these two steps are necessary because numpy sees the data as 3-dim array
y_train = y_train[:, :, 0]
# train the model
model.fit(x_train, y_train, epochs=con.eps)
# As above, create solution vectors, this time for test data
sol = []
for i in range(len(wordstest)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(wordstest[i][-1])] = 0.99
    sol.append(soli)
    wordstest[i] = wordstest[i][:-1]
inputs = []
# convert test data to input vectors
for i in range(nTrain):
    word = wordstest[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1))
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.getnumber(c)] = 1
    inputs.append(wordlist)
x_test = numpy.array(inputs)
y_test = numpy.array(sol[0:nTrain])
x_test = x_test[:, :, 0]
y_test = y_test[:, :, 0]
# test the model
x = model.evaluate(x_test, y_test)
print(x)
while True:
    input_word = input("Please enter a word:")
    querywords = [con.getlist(input_word)]
    qw = numpy.array(querywords)
    qw = qw[:, :, 0]
    pred_vect = model.predict(qw)
    max_val = numpy.max(pred_vect)
    print(numpy.argmax(pred_vect))
    # the next line is used to suppress a warning about type mismatch in line 113 (int vs ndarray[int])
    # noinspection PyTypeChecker
    max_lang = langdict[numpy.argmax(pred_vect)]
    print("I am ", max_val*100, "% certain ", input_word, " is ", max_lang)
    print(pred_vect)
