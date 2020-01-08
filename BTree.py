import pickle
from News import getNewsList
import math


class Node:
    def __init__(self, term, frequency, postingsList):
        self.term = term
        self.collectionFrequency = 0
        self.frequency = frequency   # how many docs (postingslist length)
        self.postingsList = postingsList
        self.leftChild = None
        self.rightChild = None
        self.idf = 0

    def cal_tf(self, document):
        frequency, index = self.cal_freq(document)
        tf = 1 + math.log10(frequency)
        self.addToPosting(tf, index)

    def cal_freq(self, docID):
        counter = 0
        index = 0
        postingsList = self.postingsList
        for i in range(0, len(postingsList)):
            term_pos = postingsList[i]
            if term_pos[0][0] == docID:
                index = i
                counter = len(term_pos) - 1
                break
        return counter, index

    def addToPosting(self, tf, index):
        self.postingsList[index][0][1] = tf


def compareNodes(node1, node2):
    if node1.term > node2.term:
        return 1
    elif node1.term == node2.term:
        return 0
    else:
        return -1


def compareTermWithNode(term, node2):
    if term > node2.term:
        return 1
    elif term == node2.term:
        return 0
    else:
        return -1


def cal_idf(node):
    N = len(getNewsList())
    node.idf = math.log10(N / node.frequency)


def calAllIdf(node):
    cal_idf(node)
    if not (node.leftChild is None):
        calAllIdf(node.leftChild)
    if not (node.rightChild is None):
        calAllIdf(node.rightChild)


class BTree:
    postingslists = []

    def __init__(self, root):
        self.root = root
        self.size = 0
        self.collectionSize = 0

    def getAllPL(self):
        return self.postingslists

    def getPostingsList(self, term):
        currentNode = self.root
        while not (currentNode is None):
            comparedValue = compareTermWithNode(term, currentNode)
            if comparedValue > 0:
                currentNode = currentNode.rightChild
            elif comparedValue < 0:
                currentNode = currentNode.leftChild
            else:
                return currentNode.postingsList
        return []

    def getDocIDs(self, term):
        postingsList = self.getPostingsList(term)
        docsList = []
        for docList in postingsList:
            docsList.append(docList[0][0])
        return docsList

    def addOccurrence(self, word, docID, position):
        self.collectionSize += 1
        currentNode = self.root
        while not (currentNode is None):
            comparedValue = compareTermWithNode(word, currentNode)
            if comparedValue > 0:
                parentNode = currentNode
                currentNode = currentNode.rightChild
                if currentNode is None:
                    parentNode.rightChild = Node(word, 1, [[[docID, 0], position]])
                    self.size += 1
                    return parentNode.rightChild
            elif comparedValue < 0:
                parentNode = currentNode
                currentNode = currentNode.leftChild
                if currentNode is None:
                    parentNode.leftChild = Node(word, 1, [[[docID, 0], position]])
                    self.size += 1
                    return parentNode.leftChild
            else:
                currentNode.collectionFrequency += 1
                postings = currentNode.postingsList
                doc = postings[len(postings) - 1]
                if doc[0][0] == docID:
                    doc.append(position)
                else:
                    currentNode.frequency = currentNode.frequency + 1
                    postings.append([[docID, 0], position])
                return currentNode

    def getNode(self, term):
        currentNode = self.root
        while not (currentNode is None):
            comparedValue = compareTermWithNode(term, currentNode)
            if comparedValue > 0:
                currentNode = currentNode.rightChild
            elif comparedValue < 0:
                currentNode = currentNode.leftChild
            else:
                return currentNode
        return None


def storeDictionary(dictionary):
    with open('InvertedIndex/dictionary.pickle', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadDictionary():
    file = open('InvertedIndex/dictionary.pickle', 'rb')
    variable = pickle.load(file)
    file.close()
    return variable
