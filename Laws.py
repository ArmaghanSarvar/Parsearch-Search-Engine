import matplotlib.pyplot as plot
from Heap import pushDocument
from Heap import popDocument
from News import getNewsList
import math
import pickle
from os import listdir
from os.path import isfile, join


heapDataSet = []


def heap(dictionary):
    heapDataSet.append([math.log10(dictionary.size), math.log10(dictionary.collectionSize)])


def storeHeapDataSet():
    with open('Laws/heap' + str(len(getNewsList())) + '.pickle', 'wb') as handle:
        pickle.dump(heapDataSet, handle, protocol=pickle.HIGHEST_PROTOCOL)


def showHeap():
    M = []
    T = []
    files = [f for f in listdir('Laws') if isfile(join('Laws', f))]
    for file in files:
        if file.startswith('heap'):
            file = open('Laws/' + file, 'rb')
            variable = pickle.load(file)
            for pair in variable:
                M.append(pair[0])
                T.append(pair[1])
            file.close()
    M.sort()
    T.sort()
    plot.plot(T, M)
    plot.show()


def showZipf(dictionary):
    cfs = []
    ranks = []
    iterate(dictionary.root)
    for i in range(0, min(10000, dictionary.size)):
        element = popDocument()
        ranks.append(math.log10(i + 1))
        cfs.append(math.log10(element[1]))

    plot.plot(ranks, cfs)
    plot.show()


def iterate(node):
    if node is None:
        return
    pushDocument(node.term, node.collectionFrequency)
    iterate(node.leftChild)
    iterate(node.rightChild)
