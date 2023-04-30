import numpy

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
list_of_langs = ["afr", "bos", "cze", "dan", "dut", "eng", "est", "fin", "fre", "ger", "hrv", "hun", "ice",
                 "ita", "lav", "lit", "nor", "pol", "por", "slk", "slv", "spa", "srp", "swe", "ukr"]
num_letters = len(alphabet) + 1
max_letters = 12
words_per_language = 10000
eps = 30


def get_index_of_letter(x):
    """
    Returns the index of a given character. If the character is not in the alphabet, assign index len(alphabet)
    :param x: character
    :return: index of the character in alphabet or len(alphabet) if not in alphabet
    """
    x = x.lower()
    if x in alphabet:
        return alphabet.get(x)
    else:
        with open("data/special_chars.txt", "a", encoding="utf-8") as file:
            file.write(x + "\n")
        return len(alphabet)


def get_word_vector(word):
    """
    Converts a word into a list of size num_letters*max_letters um.
    :param word:
    :return:
    """
    word = word[0:max_letters].lower()
    wordlist = numpy.zeros((num_letters * max_letters, 1)) + 0.01
    for i, c in enumerate(word):
        wordlist[i * num_letters + get_index_of_letter(c)] = 0.99
    return wordlist
