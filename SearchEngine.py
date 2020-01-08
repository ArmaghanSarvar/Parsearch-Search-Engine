import pickle

from News import getNewsList
from Tokenizer import tokenize
from Tokenizer import invalidToken
from Normalizer import normalize
from BTree import Node
from BTree import BTree
from BTree import calAllIdf
from BTree import storeDictionary
from BTree import loadDictionary
from RankedBased import loadNormFactors
from RankedBased import finalizeResults
from RankedBased import getResults
from RankedBased import getTf
import Laws
import math

dictionary = None
normalizationFactorsScheme1 = []
normalizationFactorsScheme2 = []
normalizationFactorsScheme3 = []


def constructInvertedIndex():
    global dictionary
    dictionary = BTree(Node("سسسسسس", 1, []))
    nodesList = []
    docCounter = 0
    for news in getNewsList():
        nodes = {}
        position = 0
        for term in tokenize(normalize(news.content), check_finglish):
            if term != invalidToken:
                nodes[dictionary.addOccurrence(term, news.id, position)] = True
            position += 1
        nodesList.append(nodes)
        for node in nodes:
            node.cal_tf(news.id)
        docCounter += 1
        if docCounter % 20 == 0:
            Laws.heap(getDictionary())
    calAllIdf(dictionary.root)

    i = 0
    for news in getNewsList():  # calculate the documents' normalize factors for 3 scoring schemes
        nodes = nodesList[i]
        sum_of_squares_1 = 0
        sum_of_squares_2 = 0
        sum_of_squares_3 = 0
        for node in nodes.keys():
            sum_of_squares_1 += math.pow((getTf(news.id, node.postingsList) - 1) * node.idf, 2)
            sum_of_squares_2 += math.pow(getTf(news.id, node.postingsList), 2)
            sum_of_squares_3 += math.pow(getTf(news.id, node.postingsList) * node.idf, 2)
        normalizationFactorsScheme1.append(math.sqrt(sum_of_squares_1))
        normalizationFactorsScheme2.append(math.sqrt(sum_of_squares_2))
        normalizationFactorsScheme3.append(math.sqrt(sum_of_squares_3))
        i += 1

    Laws.storeHeapDataSet()
    storeDictionary(dictionary)
    storeNormFactors()


def storeNormFactors():
    with open('InvertedIndex/normFactors1.pickle', 'wb') as handle:
        pickle.dump(normalizationFactorsScheme1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('InvertedIndex/normFactors2.pickle', 'wb') as handle:
        pickle.dump(normalizationFactorsScheme2, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('InvertedIndex/normFactors3.pickle', 'wb') as handle:
        pickle.dump(normalizationFactorsScheme3, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadInvertedIndex(isRankedBased):
    global dictionary
    dictionary = loadDictionary()
    if isRankedBased:
        loadNormFactors()


def intersect(pl_list):
    if len(pl_list) == 0:
        return []
    if len(pl_list) == 1:
        return pl_list[0]
    answer = []
    pointer0 = 0
    pointer1 = 0
    while pointer0 < len(pl_list[0]) and pointer1 < len(pl_list[1]):
        if pl_list[0][pointer0] == pl_list[1][pointer1]:
            answer.append(pl_list[0][pointer0])
            pointer0 += 1
            pointer1 += 1
        elif pl_list[0][pointer0] < pl_list[1][pointer1]:
            pointer0 += 1
        else:
            pointer1 += 1
    pl_list[1] = answer
    return intersect(pl_list[1:])


def AND_NOT(pl_list0, pl_list1):
    answer = []
    pointer0 = 0
    pointer1 = 0
    while pointer0 < len(pl_list0) and pointer1 < len(pl_list1):
        if pl_list0[pointer0][0] == pl_list1[pointer1][0]:
            pointer0 += 1
            pointer1 += 1
        elif pl_list0[pointer0][0] < pl_list1[pointer1][0]:
            answer.append(pl_list0[pointer0])
        else:
            pointer1 += 1
    while pointer0 < len(pl_list0):
        answer.append(pl_list0[pointer0])
        pointer0 += 1
    return answer


def NOT(term_pl):
    all_docs = []
    pointer = 0
    if len(term_pl) == 0:
        for d in range(0, len(getNewsList())):
            all_docs.append(d)
    else:
        for d in range(0, len(getNewsList())):
            if d != term_pl[pointer]:
                all_docs.append(d)
            else:
                pointer += 1
                if pointer == len(term_pl):
                    d += 1
                    while d < len(getNewsList()):
                        all_docs.append(d)
                        d += 1
                    break
    return all_docs


def phraseQuery(pl_list, distance):
    if len(pl_list) == 0:
        return []

    # Stop words processes

    if len(pl_list) == 1:
        if len(pl_list[0]) >= 1:
            if len(pl_list[0][0]) >= 1:
                if pl_list[0][0][0] == -1:    # the DocID of Stop words
                    return []
    else:
        if len(pl_list[0]) >= 1:
            if len(pl_list[0][0]) >= 1:
                if pl_list[0][0][0] == -1:
                    return phraseQuery(pl_list[1:], distance)
        if len(pl_list[1]) >= 1:
            if len(pl_list[1][0]) >= 1:
                if pl_list[1][0][0] == -1:
                    pl_list[1] = pl_list[0]
                    return phraseQuery(pl_list[1:], distance + 1)

    # Done

    if len(pl_list) == 1:
        return pl_list[0]

    answer = []
    pointer0 = 0
    pointer1 = 0
    while pointer0 < len(pl_list[0]) and pointer1 < len(pl_list[1]):
        if pl_list[0][pointer0][0][0] == pl_list[1][pointer1][0][0]:
            pointer00 = 1  # after docID
            pointer11 = 1
            while pointer00 < len(pl_list[0][pointer0]) and pointer11 < len(pl_list[1][pointer1]):
                if pl_list[1][pointer1][pointer11] - pl_list[0][pointer0][pointer00] == distance:
                    answer.append(pl_list[1][pointer1])
                    pointer00 += 1
                    pointer11 += 1
                    break

                elif pl_list[0][pointer0][pointer00] > pl_list[1][pointer1][pointer11]:
                    pointer11 += 1

                else:
                    pointer00 += 1
            pointer0 += 1
            pointer1 += 1
        elif pl_list[0][pointer0][0][0] < pl_list[1][pointer1][0][0]:
            pointer0 += 1
        else:
            pointer1 += 1
    pl_list[1] = answer
    return phraseQuery(pl_list[1:], 1)


def get_docIDs(intersect_pl_results):
    results = []
    for i in range(0, len(intersect_pl_results)):
        if intersect_pl_results[i][0] not in results:
            results.append(intersect_pl_results[i][0])
    return results


def query(pl_list, tokens, isRankedBased):
    if not pl_list and not isRankedBased:
        return []

    results = intersect(pl_list)  # in rankedBased, only the lists of NOT and Phrase inputs

    if isRankedBased:
        for docID in results:
            # Only the Docs that have at least one query term get + 0.5 bonus
            if getNewsList()[docID].hasQueryTerm:
                getNewsList()[docID].score += 0.5
        finalizeResults()   # Top K
        results = getResults()  # it is nothing but a return :/

    structuredResults = []
    for result in results:
        structuredResults.append(getNewsList()[result].structuredFormatResultsPage(tokens))

    return structuredResults


def check_finglish(token):   # check the equal persian(finglish) term if the english input is not in dic
    if not dictionary.getPostingsList(token):
        finglish_term = ""
        for character in token:
            try:
                finglish_term += mapping_dic[character]
            except KeyError:
                return token
        return finglish_term
    return token


def load_mapping_dic():
    file = open('Resources/FinglishWords/mapping_dic.pickle', 'rb')
    variable = pickle.load(file)
    file.close()
    return variable


def getDictionary():
    return dictionary


mapping_dic = load_mapping_dic()
