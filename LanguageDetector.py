import random
import tensorflow as tf
import numpy
import config as con

max_letters = 12
words_per_language = 30000
num_letters = 123
listoflangs = ["bos", "cze", "dan", "dut", "eng", "fin", "fre", "ger", "hrv", "hun", "ice",
               "ita", "nor", "pol", "por", "slk", "slv", "spa", "srp",  "swe", "ukr"]
user_select = True
langs = []
# Ask user to select the languages he wants the model to learn.
while user_select:
    print("Zur Auswahl stehen die Sprachen ", listoflangs)
    selected_lang = input("Bitte Sprache eingeben.")
    if selected_lang == "":
        user_select = False
    elif selected_lang not in listoflangs:
        print("Sprache nicht gefunden oder bereits gewählt.")
    else:
        listoflangs.remove(selected_lang)
        langs.append(selected_lang)
        if len(langs) >= 10:
            print("Maximal 10 Sprachen möglich!")
            user_select = False
            break
nTrain = len(langs)*words_per_language
langdict = {}
for lang in langs:
    langdict[langs.index(lang)] = lang
print(langdict)
wordstrain = []
wordstest = []
for lang in langs:
    langfile = "data/"+lang+"_large.txt"
    langlist = []
    with open(langfile, 'r') as file:
        for line in file.readlines():
            langlist.append(line[0:max_letters].strip().lower() + str(langs.index(lang)))
    random.shuffle(langlist)
    wordstrain = wordstrain + langlist[0:words_per_language]
    wordstest = wordstest + langlist[words_per_language:2*words_per_language]
print(wordstrain[100])
print(wordstrain[20100])
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
sol = []
for i in range(len(wordstrain)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(wordstrain[i][-1])] = 1
    sol.append(soli)
    wordstrain[i] = wordstrain[i][:-1]
inputs = []
for i in range(nTrain):
    word = wordstrain[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1)) + 0.01
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.getnumber(c)] = 0.99
    inputs.append(wordlist)
x_train = numpy.array(inputs)
y_train = numpy.array(sol[0:nTrain])
x_train = x_train[:, :, 0]
y_train = y_train[:, :, 0]
model.fit(x_train, y_train, epochs=con.eps)
sol = []
for i in range(len(wordstest)):
    soli = numpy.zeros((len(langs), 1)) + 0.01
    soli[int(wordstest[i][-1])] = 1
    sol.append(soli)
    wordstest[i] = wordstest[i][:-1]
inputs = []

for i in range(nTrain):
    word = wordstest[i]
    wordlist = numpy.zeros((con.num_letters * con.max_letters, 1)) + 0.01
    for j, c in enumerate(word):
        wordlist[j * con.num_letters + con.getnumber(c)] = 0.99
    inputs.append(wordlist)
x_test = numpy.array(inputs)
y_test = numpy.array(sol[0:nTrain])
x_test = x_test[:, :, 0]
y_test = y_test[:, :, 0]
x = model.evaluate(x_test, y_test)
print(x)
while True:
    input_word = input("Bitte Wort eingeben:")
    querywords = [con.getlist(input_word)]
    qw = numpy.array(querywords)
    qw = qw[:, :, 0]
    pred_vect = model.predict(qw)
    max_val = numpy.max(pred_vect)
    print(numpy.argmax(pred_vect))
    # noinspection PyTypeChecker
    max_lang = langdict[numpy.argmax(pred_vect)]
    print("Ich bin mir zu", max_val*100, "% sicher, dass ", input_word, " ", max_lang, " ist.")
    print(pred_vect)
