import pickle

dictionary = {
    'q': 'ض',
    'w': 'ص',
    'e': 'ث',
    'r': 'ق',
    't': 'ف',
    'y': 'غ',
    'u': 'ع',
    'i': 'ه',
    'o': 'خ',
    'p': 'ح',
    '[': 'ج',
    ']': 'چ',
    '\\': 'پ',
    'a': 'ش',
    's': 'س',
    'd': 'ی',
    'f': 'ب',
    'g': 'ل',
    'h': 'ا',
    'j': 'ت',
    'k': 'ن',
    'l': 'م',
    ';': 'ک',
    '\'': 'گ',
    'z': 'ظ',
    'x': 'ط',
    'c': 'ز',
    'v': 'ر',
    'b': 'ذ',
    'n': 'د',
    'm': 'ئ',
    ',': 'و',
    'C': 'ژ'
}


def store_dictionary():
    with open('Resources/FinglishWords/mapping_dic.pickle', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)


# store_dictionary()
