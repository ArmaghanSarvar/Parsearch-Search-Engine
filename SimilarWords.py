import pickle


def loadSimilarWords():
    file = open('Resources/SimilarWords/similar_words.pickle', 'rb')
    variable = pickle.load(file)
    file.close()
    return variable


def getSimilarWord(token):
    if token in similarWords:
        return similarWords[token]
    else:
        return token


def storeSimilarWords():
    dictionary = {'قران': 'قرآن',
                  'مسئول': 'مسوول',
                  'مسؤول': 'مسوول',
                  "چنانچه": "چنان‌چه",
                  'مهاباد': 'مهآباد',
                  'آئین': 'آیین',
                  'رئیس': 'رییس',
                  'ارائه': 'ارایه',
                  'طهران': 'تهران',
                  'تائید': 'تایید',
                  'شمبه': 'شنبه',
                  'دوشمبه': 'دوشنبه',
                  'تأکید': 'تاکید',
                  "بنابرین": "بنابراین",
                  "ذغال": "زغال",
                  'مؤسسه': 'موسسه'
                  }

    with open('Resources/SimilarWords/similar_words.pickle', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)


similarWords = loadSimilarWords()
