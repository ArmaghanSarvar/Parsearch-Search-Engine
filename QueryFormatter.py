import re
from Stemmer import stem
from SearchEngine import phraseQuery
from SearchEngine import NOT
from SearchEngine import check_finglish
from SearchEngine import getDictionary
from Normalizer import normalize
from Tokenizer import isPunctuation
from Tokenizer import isNumber
from Tokenizer import checkIfSegmented
from SimilarWords import getSimilarWord
from StopWords import isStopWord
from SpellChecker import autoCorrect
from RankedBased import calCosSimilarity


def convertToPostingsLists(text, level, isRankedBased):
    answer = []   # return found DocIDs
    tokens = []

    while True:     # NOT Operator
        result = re.search(r"!([^\s\"]|(\"[^\"]*\"))+", text)
        if result is not None:
            token = result.group()
            returned_list, nothing = convertToPostingsLists(token[1:].strip(), level + 1, isRankedBased)
            if len(returned_list) != 0:
                if type(returned_list[0]) is returned_list:
                    answer.append(NOT(returned_list[0][0]))
                else:
                    answer.append(NOT(returned_list[0]))
            text = text.replace(token, "", 1)
        else:
            break

    phrases = re.findall(r"\"[^\"]+\"", text)
    for phrase in phrases:       # Phrase Query
        docs = []
        for token in normalize(phrase[1:-1]).split():
            if isStopWord(token) or isPunctuation(token) or isNumber(token):
                docs.append([[-1]])
                continue
            token = check_finglish(token)
            tokens.append(token)
            token = getSimilarWord(token)
            token = autoCorrect(token)
            token = stem(token)
            docs.append(getDictionary().getPostingsList(token))
        docsList = []
        for positionList in phraseQuery(docs, 1):
            docsList.append(positionList[0][0])
        answer.append(docsList)
        text = text.replace(phrase, "")

    text = normalize(text)
    splits = text.split()
    i = 0
    nodes = []
    while i != len(splits):
        token = splits[i]
        segmentedCandidates = checkIfSegmented(token)
        while len(segmentedCandidates) != 0:
            candidateSplit = segmentedCandidates[0][0]
            matched = True
            for j in range(1, len(candidateSplit)):
                if splits[i + j] != candidateSplit[j]:
                    matched = False
                    break
            if matched:
                i += len(candidateSplit) - 1
                token = segmentedCandidates[0][1]
                break
            else:
                segmentedCandidates.remove(0)
        i += 1
        if isStopWord(token) or isPunctuation(token) or isNumber(token):
            continue    # jump to the next token!
        token = check_finglish(token)
        tokens.append(token)
        token = getSimilarWord(token)
        token = autoCorrect(token)
        token = stem(token)
        if isRankedBased and level == 0:  # check level not to go further in recursive operator (NOT) for scoring
            node = getDictionary().getNode(token)
            if node is not None:   # query term in dic
                nodes.append(node)
        else:  # when not rankedbased, we add the lists of normal query terms to the answer list too
            answer.append(getDictionary().getDocIDs(token))
    if isRankedBased and level == 0:   # after the whole query terms are processed
        calCosSimilarity(nodes)
    return answer, tokens


def extractSpecialOperators(text):   # for the category and source operators (last phase)
    category = ""
    source = ""
    results = re.findall(r"cat:\w+", text)
    for token in results:
        category = token[4:]
        text = text.replace(token, "")

    results = re.findall(r"source:[\w.\-]+", text)
    for token in results:
        source = token[7:]
        text = text.replace(token, "")

    return text.strip(), category, source
