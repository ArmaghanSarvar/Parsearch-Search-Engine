from Stemmer import stem
from SpellChecker import autoCorrect
from StopWords import isStopWord
import string

invalidToken = r"/^*|\$"
punctuations = string.punctuation + "؛»«،؟"

commonlySegmentedLists = {
    "فی ما بین": "فی‌مابین",
    "فی مابین": "فی‌مابین",
    "چنان چه": "چنان‌چه",
    "بنا بر این": "بنابراین",
    "بنابر این": "بنابراین",
    "بنا براین": "بنابراین",
    "بنا برین": "بنابراین",
    "مع ذلک": "مع‌ذلک",
    "خبرگزاری ج . ا .": "خبرگزاری جمهوری اسلامی",
    "علی‌ای حال": "علی‌ای‌حال",
    "علی ای حال": "علی‌ای‌حال"
}


def checkIfSegmented(token):
    candidates = []
    for word in commonlySegmentedLists:
        splits = word.split()
        if token == splits[0]:
            candidates.append([splits, commonlySegmentedLists[word]])
    return candidates


def isSeparator(char):
    return not char.isalpha()


def isPunctuation(token):
    for char in token:
        if char not in punctuations:
            return False
    return True


def isNumber(token):
    for char in token:
        if not char.isdigit():
            return False
    return True


def processToken(token, check_finglish):
    if len(token.strip("\u200c")) != 0:
        token = token.strip("\u200c")
    if isNumber(token) or isPunctuation(token) or isStopWord(token) or token.startswith("http"):
        return invalidToken
    if check_finglish:
        token = check_finglish(token)
    return autoCorrect(stem(token))


def tokenize(text, check_finglish):
    # In Normalizer we have made the punctuations a different segment. here just by space
    temp_list = text.strip().split()
    token_list = []
    i = 0
    while i < len(temp_list):
        token = temp_list[i]
        for word in commonlySegmentedLists:
            matched = True
            segments = word.split()
            for j in range(0, len(segments)):
                if i + j >= len(temp_list):
                    break
                if temp_list[i + j] != segments[j]:
                    matched = False
                    break
            if matched:
                token = commonlySegmentedLists[word]
                i += len(segments) - 1
                break
        token_list.append(token)
        i += 1
    token_list = [processToken(x, check_finglish) for x in token_list]
    return token_list
