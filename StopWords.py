import pickle


def loadStopWords():
    file = open('Resources/StopWords/stop_words.pickle', 'rb')
    variable = pickle.load(file)
    file.close()
    return variable


def isStopWord(token):
    return token in stopWords


def createStopWords(currentNode):
    list = []
    if currentNode is not None:
        list.append((currentNode.term, currentNode.frequency))
        list += createStopWords(currentNode.leftChild)
        list += createStopWords(currentNode.rightChild)

    return list


def storeStopWords(list):
    with open('Resources/StopWords/stop_words.pickle', 'wb') as handle:
        pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)


def sortStopWords(list):
    list.sort(key=key, reverse=True)
    return list


def key(entry):
    return entry[1]


stopWords = loadStopWords()
