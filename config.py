import numpy


languages = {0: "Englisch", 1: "Deutsch", 2: "Französisch", 3: "Spanisch", 4: "Schwedisch",
             5: "Polnisch", 6: "Finnisch"}
# contains "all" lowercase letters needed to write all european languages written in roman letters, according to
# http://recherche-redaktion.de/sprachen/paneurop.htm some of them are only used in livonian or esperanto
alphabet = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12,
            'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
            'z': 25, 'á': 26, 'ă': 27, 'ä': 28, 'à': 29, 'æ': 30, 'ā': 31, 'ą': 32, 'å': 33, 'ã': 34, 'â': 35, 'ć': 36,
            'č': 37, 'ç': 38, 'ċ': 39, 'ĉ': 40, 'ď': 41, 'ḑ': 42, 'đ': 43, 'é': 44, 'ě': 45, 'ë': 46, 'è': 47, 'ē': 48,
            'ę': 49, 'ė': 50, 'ê': 51, 'ğ': 52, 'ģ': 53, 'ġ': 54, 'ĝ': 55, 'ħ': 56, 'ĥ': 57, 'í': 58, 'ï': 59, 'ì': 60,
            'ĳ': 61, 'ī': 62, 'į': 63, 'ı': 64, 'î': 65, 'ĵ': 66, 'ķ': 67, 'ĺ': 68, 'ľ': 69, 'ļ': 70, 'ŀ': 71, 'ł': 72,
            'ń': 73, 'ň': 74, 'ņ': 75, 'ñ': 76, 'ó': 77, 'ő': 78, 'ö': 79, 'ȫ': 80, 'ò': 81, 'œ': 82, 'ō': 83, 'ọ': 84,
            'ȯ': 85, 'ø': 86, 'õ': 87, 'ȭ': 88, 'ǫ': 89, 'ô': 90, 'ŕ': 91, 'ř': 92, 'ŗ': 93, 'ś': 94, 'š': 95, 'ş': 96,
            'ș': 97, 'ß': 98, 'ŝ': 99, 'ť': 100, 'ţ': 101, 'ț': 102, 'ŧ': 103, 'ú': 104, 'ű': 105, 'ŭ': 106, 'ü': 107,
            'ù': 108, 'ū': 109, 'ų': 110, 'ů': 111, 'û': 112, 'ý': 113, 'ÿ': 114, 'ȳ': 115, 'ź': 116, 'ž': 117,
            'ż': 118, 'ŋ': 119, 'ð': 120, 'þ': 121
            }
num_letters = len(alphabet) + 1
num_lang = 7
max_letters = 12
words_per_language = 20000
eps = 30
nTrain = num_lang * words_per_language


def getnumber(x):
    """
    Gibt zu 'jedem' Buchstaben eine Zahl zurück. Bildet im wesentlichen eine Map
    :param x:
    :return:
    """
    x = x.lower()
    if x in alphabet:
        return alphabet.get(x)
    else:
        with open("data/special_chars.txt", "a", encoding="utf-8") as file:
            file.write(x+"\n")
        return len(alphabet)
    # # Normales Alphabet
    # if 97 <= ord(x) <= 122:
    #     return ord(x)-97
    # elif x == 'ä':
    #     return 27
    # elif x == 'ö':
    #     return 28
    # elif x == 'ü':
    #     return 29
    # elif x == 'ß':
    #     return 30
    # elif x == 'é':
    #     return 31
    # elif x == 'à':
    #     return 32
    # elif x == 'î':
    #     return 33
    # elif x == 'è':
    #     return 34
    # elif x == 'ó':
    #     return 35
    # elif x == 'å':
    #     return 36
    # elif x == 'ò':
    #     return 37
    # elif x == 'ł':
    #     return 38
    # elif x == 'ż':
    #     return 39
    # elif x == 'ñ':
    #     return 40
    # elif x == 'ą':
    #     return 41
    # elif x == 'í':
    #     return 42
    # elif x == 'á':
    #     return 43
    # elif x == 'ś':
    #     return 44
    # elif x == 'ń':
    #     return 45
    # elif x == 'â':
    #     return 46
    # elif x == '-':
    #     return 47
    # elif x == 'ę':
    #     return 48
    # elif x == ' ':
    #     return 49
    # elif x == 'ê':
    #     return 50
    # elif x == 'ć':
    #     return 51
    # elif x == 'ø':
    #     return 52
    # elif x == 'æ':
    #     return 53
    # elif x == '\'':
    #     return 54
    # elif x == "č":
    #     return 55
    # elif x == "ě":
    #     return 56
    # elif x == "ř":
    #     return 57
    # elif x == "š":
    #     return 58
    # elif x == "ý":
    #     return 59
    # elif x == "ž":
    #     return 60
    # elif x == "ð":  # ice
    #     return 61
    # elif x == "þ":  # ice
    #     return 62
    # elif x == "ã":  # por
    #     return 63
    # elif x == "ç":  # por/fre
    #     return 64
    # elif x == "ú":  # spa/cze
    #     return 65
    # elif x == "ő":  # hun
    #     return 66
    # elif x == 'ź':  # pol
    #     return 67
    # elif x == 'ů':  # cze
    #     return 68
    # elif x == 'ť':  # cze/slk
    #     return 69
    # elif x == 'õ':  # por
    #     return 70
    # elif x == 'đ':  # hrv/srp
    #     return 71
    # elif x == 'ë':  # dut/afr
    #     return 72
    # elif x == 'ï':
    #     return 73   # dut/afr/fre
    # elif x == 'ň':
    #     return 74   # slk
    # else:
    #     with open("data/special_chars.txt", "a", encoding="utf-8") as file:
    #         file.write(x+"\n")
    #     return 75


def getlist(word):
    """
    Wandelt ein Wort in eine Liste der Länge num_letters*max_letters um.
    :param word:
    :return:
    """
    word = word[0:max_letters].lower()
    wordlist = numpy.zeros((num_letters*max_letters, 1)) + 0.01
    for i, c in enumerate(word):
        wordlist[i * num_letters + getnumber(c)] = 0.99
    return wordlist
