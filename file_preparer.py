'''
Script to extract the needed information from the files included in the wortschatz Universität Leipzig:
https://wortschatz.uni-leipzig.de
Goal of this script is NOT the check whether the words in the dataset are actually from this language, but to filter out
words containing symbols not used in the language
'''

import re

filename = "data/lit_newscrawl_2016_300K-words.txt"
words = []
minLen = 5
maxLen = 20
pattern = "^[a-ząčęėįšųūž]+$"  # put alphabet of language inside []
with open(filename, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        lineSplit = line.split("\t")
        word = lineSplit[1]  # word is in the second column
        if len(word) < minLen or len(word) > maxLen:  # filter out short or very long words
            continue
        word = word.lower()  # only use lowercase letters

        if not re.match(pattern, word):  # remove all words that contain symbols this language doesn't have
            print(word)
            continue
        words.append(word)
print(len(words))

with open("data/lit_large.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(words))
