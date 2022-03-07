# import tensorflow as tf
import numpy as np
import random
languages = ["ger", "eng", "fra"]
langdict = {"ger": 0, "eng": 1, "fra": 2}
alphabet = {"a":1, "b":2, "c":3, "d":4,"e":5,"f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14,
            "o":15, "p":16, "q":17, "r":18, "s":19, "t":20, "u":21, "v":22, "w":23, "x":24,"y":25, "z":26, "ä": 27,
            "ö": 28, "ü": 29, "à": 30, "â":31, "æ": 32, "ç": 33, "é":34, "è":35, "ë":36, "î":37, "ï":38, "ô": 39,
            "œ": 40, "ù":41, "û":42, "ÿ": 43}
words = []
training_words = []
test_words = []
for lang in languages:
    with open("data/"+lang+"_10k.txt", "r", encoding="utf-8") as file:
        words = file.readlines()
        random.shuffle(words)
        words_to_add = [word.strip() + " " + str(langdict[lang]) for word in words]
        training_words = training_words + words_to_add[0:7000]
        test_words = test_words + words_to_add[7000:10000]

print(training_words[0])
print(training_words[8000])
print(training_words[15000])
