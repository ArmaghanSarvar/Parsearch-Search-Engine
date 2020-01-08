import pickle
from News import getNewsList
import math
import Heap
scheme = 3

# two index elimination methods
indexEliminationIdfThreshold = 0.3
indexEliminationManyThreshold = 0   # the document can have up to this number lack in query terms

maxFreq = 0
k = 40   # how many best docs
results = []


def loadNormFactors():
    global normalizationFactors
    file = open('InvertedIndex/normFactors' + str(scheme) + '.pickle', 'rb')
    normalizationFactors = pickle.load(file)
    file.close()


def calW_tq(node, frequency):   # query weight
    if scheme == 1:
        return (0.5 + 0.5 * frequency / maxFreq) * node.idf
    elif scheme == 2:
        return math.log10(1 + len(getNewsList()) / node.frequency)
    else:
        return (1 + math.log10(frequency)) * node.idf


def calW_td(tf, node):   # doc weight
    if scheme == 1:
        return node.idf * (tf - 1)
    elif scheme == 2:
        return tf
    else:
        return tf * node.idf


def calMaxFreq(nodes):
    global maxFreq
    maxFreq = 0
    freqList = {}
    for node in nodes:
        freqList[node] = 0
    for node in nodes:
        freqList[node] += 1
    for key in freqList.keys():
        maxFreq = max(maxFreq, freqList[key])


def getDocIDs(pl):
    docsList = []
    for docList in pl:
        docsList.append(docList[0][0])
    return docsList


def getTf(document, pl):
    for docList in pl:
        if docList[0][0] == document:
            return docList[0][1]


def checkManyEliminationCondition(newsID, nodes):
    counter = 0
    threshold = len(nodes) - indexEliminationManyThreshold
    for node in nodes:
        if newsID in getDocIDs(node.postingsList):
            counter += 1
    return counter >= threshold


def calCosSimilarity(nodes):
    global results
    results = []
    Heap.clearHeap()   # for each new query we should reset
    calMaxFreq(nodes)
    for news in getNewsList():  # again, reset
        news.score = 0
        news.hasQueryTerm = False

    eliminatedDocuments = {}
    nodesProcessed = []
    for node in nodes:
        if node in nodesProcessed:
            continue
        if node.idf < indexEliminationIdfThreshold:
            continue
        # print(node.term, node.idf)
        nodesProcessed.append(node)
        frequency = 0
        for node2 in nodes:
            if node == node2:
                frequency += 1
        wtq = calW_tq(node, frequency)
        postingsList = node.postingsList
        for news in getDocIDs(postingsList):
            getNewsList()[news].hasQueryTerm = True
            if news in eliminatedDocuments:
                continue
            if not checkManyEliminationCondition(news, nodes):
                eliminatedDocuments[news] = True
                getNewsList()[news].score = 0
                continue
            tf = getTf(news, postingsList)
            wtd = calW_td(tf, node)
            getNewsList()[news].score += wtd * wtq

    for i in range(0, len(getNewsList())):
        if normalizationFactors[i] == 0:   # division by zero
            getNewsList()[i].score = 0
            continue
        getNewsList()[i].score = getNewsList()[i].score / normalizationFactors[i]


def finalizeResults():
    for news in getNewsList():   # the Docs with nonzero score added to the heap
        if news.score != 0:
            Heap.pushDocument(news.id, news.score)  # each node = DocID and its score

    for i in range(0, k):
        temp = Heap.popDocument()
        if not temp:
            continue
        results.append(temp[0])
        # print(temp[1])


def getResults():
    return results
