import pickle

nounLexPath = "Resources/Stemmer/Modified/noun_lexicon.pickle"
# nounLexPath = "Resources/Stemmer/stem_lex.pckl"
# verbLexPath = "Resources/Stemmer/verbStemDict.pckl"
verbLexPath = "Resources/Stemmer/Modified/verb_lexicon.pickle"
verbTenseMapPath = "Resources/Stemmer/Modified/verb_tense_map.pickle"
# verbTenseMapPath = "Resources/Stemmer/stem_verbMap.pckl"
irregularNounsPath = "Resources/Stemmer/Modified/irregular_nouns.pickle"
prefixListPath = "Resources/Stemmer/Modified/prefix.txt"
postfixListPath = "Resources/Stemmer/pasvand.txt"
verbTensePath = "Resources/Stemmer/verb_tense.txt"
pluralsPath = "Resources/Stemmer/mokasar.txt"

nounLexicon = None
verbLexicon = None
verbTenseMap = None
irregularNouns = None
prefixList = None
postfixList = None
verbF2P = None
verbP2F = None


def loadPickleFile(path):
    file = open(path, 'rb')
    variable = pickle.load(file)
    file.close()
    return variable


def loadFiles():
    global nounLexicon, verbLexicon, verbTenseMap, irregularNouns
    global prefixList, postfixList
    global verbF2P, verbP2F

    nounLexicon = loadPickleFile(nounLexPath)
    verbLexicon = loadPickleFile(verbLexPath)
    verbTenseMap = loadPickleFile(verbTenseMapPath)
    irregularNouns = loadPickleFile(irregularNounsPath)

    verbF2P, verbP2F = verbTenseMap[1], verbTenseMap[0]

    prefixList = set({})
    with open(prefixListPath, "r", encoding='utf-8') as file:
        content = file.readlines()
        for element in content:
            prefixList.add(element.strip())

    postfixList = set({})
    with open(postfixListPath, "r", encoding='utf-8') as file:
        content = file.readlines()
        for element in content:
            postfixList.add(element.strip())


def getStemmedNoun(word):
    if word in irregularNouns:
        return irregularNouns[word]
    else:
        return word


def isPrefix(word, prefix):
    word = word.strip("\u200c")
    return word.startswith(prefix)


def isPostfix(word, post):
    word = word.strip("\u200c")
    return word.endswith(post)


def removePrefixes(word, prefix):
    word = word.strip("\u200c")
    candidateStem = set({})
    for element in prefix:
        if word.startswith(element):
            if len(element) > 0:
                tmp = word[len(element):].strip().strip('\u200c')
            else:
                tmp = word
            candidateStem.add(tmp)
    return candidateStem


def removePostfixes(word, postfix):
    word = word.strip("\u200c")
    candidateStem = set({})
    for element in postfix:
        if word.endswith(element):
            if len(element) > 0:
                tmp = word[:-len(element)].strip().strip('\u200c')
            else:
                tmp = word
            candidateStem.add(tmp)
    return candidateStem


def selectShortest(list):
    if list.__len__() == 0:
        return ""

    word = ""
    length = 31807
    for token in list:
        if len(token) < length:
            length = len(token)
            word = token

    return word


def selectLongestInLexicons(list, lexicons):
    if list.__len__() == 0:
        return ""

    word = ""
    length = 0
    for token in list:
        if len(token) > length and token in lexicons:
            word = token
            length = len(token)

    return word


def checkIfVerb(word):
    candidateList = removePrefixes(word, ["داشتم", "داشتی", "داشت",
                                          "داشتیم", "داشتید", "داشتند"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePrefixes(new_word, ["می"])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            candidateList = removePostfixes(new_word, ["یم", "ید", "ند",
                                                       "م", "ی", ""])
            if len(candidateList) > 0:
                new_word = selectLongestInLexicons(candidateList, verbLexicon)
                if new_word:
                    if new_word in verbP2F:
                        stem = verbP2F[new_word]
                        return stem, True

    candidateList = removePrefixes(word, ["دارم", "داری", "دارد",
                                          "داریم", "دارید", "دارند"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePrefixes(new_word, ["می"])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            candidateList = removePostfixes(new_word, ["یم", "ید", "ند",
                                                       "م", "ی", "د"])
            if len(candidateList) > 0:
                new_word = selectLongestInLexicons(candidateList, verbLexicon)
                if new_word:
                    if new_word in verbF2P:
                        stem = new_word
                        return stem, True

    candidateList = removePrefixes(word, ["می", "نمی", "همی"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["یم", "ید", "ند",
                                                   "م", "ی", "د"])
        if len(candidateList) > 0:
            new_word = selectLongestInLexicons(candidateList, verbLexicon)
            if new_word:
                if new_word in verbF2P:
                    stem = new_word
                    return stem, True

    candidateList = removePrefixes(word, ["می", "نمی", "همی"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["یم", "ید", "ند",
                                                   "م", "ی", ""])
        if len(candidateList) > 0:
            new_word = selectLongestInLexicons(candidateList, verbLexicon)
            if new_word:
                if new_word in verbP2F:
                    stem = verbP2F[new_word]
                    return stem, True

    candidateList = removePostfixes(word, ["یم", "ید", "ند",
                                           "م", "ی", ""])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["بود", "باشد", "باش"])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            candidateList = removePostfixes(new_word, ["ه"])
            if len(candidateList) > 0:
                new_word = selectShortest(candidateList)
                candidateList = removePrefixes(new_word, ["ن", "", "ب"])
                if len(candidateList) > 0:
                    new_word = selectLongestInLexicons(candidateList, verbLexicon)
                    if new_word:
                        if new_word in verbP2F:
                            stem = verbP2F[new_word]
                            return stem, True

    candidateList = removePostfixes(word, ["ام", "ای", "است",
                                           "ایم", "اید", "اند"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["ه"])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            candidateList = removePrefixes(new_word, ["ن", "", "ب"])
            if len(candidateList) > 0:
                new_word = selectLongestInLexicons(candidateList, verbLexicon)
                if new_word:
                    if new_word in verbP2F:
                        stem = verbP2F[new_word]
                        return stem, True

    candidateList = removePostfixes(word, ["ام", "ای", "است",
                                           "ایم", "اید", "اند"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["ه"])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            candidateList = removePostfixes(new_word, ["بود"])
            if len(candidateList) > 0:
                new_word = selectShortest(candidateList)
                candidateList = removePostfixes(new_word, ["ه"])
                if len(candidateList) > 0:
                    new_word = selectShortest(candidateList)
                    candidateList = removePrefixes(new_word, ["ن", "", "ب"])
                    if len(candidateList) > 0:
                        new_word = selectLongestInLexicons(new_word, verbLexicon)
                        if new_word:
                            if new_word in verbP2F:
                                stem = verbP2F[new_word]
                                return stem, True

    candidateList = removePrefixes(word, ["خواه", "نخواه"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePrefixes(new_word, ["یم", "ید", "ند",
                                                  "م", "ی", "د"])
        if len(candidateList) > 0:
            new_word = selectLongestInLexicons(candidateList, verbLexicon)
            if new_word:
                if new_word in verbP2F:
                    stem = verbP2F[new_word]
                    return stem, True

    candidateList = removePrefixes(word, ["ب", "ن", ""])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePostfixes(new_word, ["یم", "ید", "ند", "م",
                                                   "ی", "د", ""])
        if len(candidateList) > 0:
            new_word = selectShortest(candidateList)
            if (isPrefix(new_word, "یا")) and (new_word not in verbLexicon):
                candidateList = removePrefixes(new_word, ["یا"])
                new_word = selectShortest(candidateList)
                new_word = "آ" + new_word
            if isPostfix(new_word, "آی") or isPostfix(new_word, "ای"):
                if new_word not in verbLexicon:
                    candidateList = removePostfixes(new_word, ["ی"])
                    new_word = selectShortest(candidateList)
            if isPrefix(new_word, "ی"):
                candidateList = removePrefixes(new_word, ["ی"])
                tmp_word = selectShortest(candidateList)
                if tmp_word and ("ا" + tmp_word) in verbLexicon:
                    new_word = "ا" + tmp_word

        if new_word and new_word in verbLexicon:
            if new_word in verbF2P:
                stem = new_word
                return stem, True

    candidateList = removePostfixes(word, ["م", "ی", "",
                                           "یم", "ید", "ند"])
    if len(candidateList) > 0:
        new_word = selectShortest(candidateList)
        candidateList = removePrefixes(new_word, ["ن", "", "ب"])
        if len(candidateList) > 0:
            new_word = selectLongestInLexicons(candidateList, verbLexicon)
            if new_word:
                if new_word in verbP2F:
                    stem = verbP2F[new_word]
                    return stem, True

    candidateList = removePostfixes(word, ["ن", "ب"])
    if len(candidateList) > 0:
        new_word = selectLongestInLexicons(candidateList, verbLexicon)
        if new_word:
            if new_word in verbP2F:
                stem = verbP2F[new_word]
                return stem, True

    return "", False


def checkIfNoun(word):
    stemCandidate = word
    candidateList = removePostfixes(word, ["م", "ت", "ش", "یم", "یت", "یش", "ون",
                                           "یتان", "یشان", "یمان",
                                           "مان", "تان", "شان", "ان"])
    if len(candidateList) > 0:
        stemCandidate = selectLongestInLexicons(candidateList, nounLexicon)
        if stemCandidate:
            newToken = stemCandidate
        else:
            newToken = selectShortest(candidateList)
        stemCandidate = newToken
    else:
        newToken = stemCandidate

    if newToken in nounLexicon:
        return getStemmedNoun(newToken), True

    candidateList = removePostfixes(word, ["ها", "ات", "های",
                                           "ان", "هایی", "ین"])
    if len(candidateList) > 0:
        stemCandidate = selectLongestInLexicons(candidateList, nounLexicon)
        if stemCandidate:
            newToken = stemCandidate
        else:
            newToken = selectShortest(candidateList)
        stemCandidate = newToken
    else:
        newToken = stemCandidate

    if newToken in nounLexicon:
        return getStemmedNoun(newToken), True

    candidateList = removePostfixes(word, ["گ"])
    if len(candidateList) > 0:
        newToken = selectShortest(candidateList)
        newToken = newToken + "ه"
        stemCandidate = newToken
    else:
        newToken = stemCandidate

    if newToken in nounLexicon:
        return getStemmedNoun(newToken), True

    candidateList = removePostfixes(word, postfixList)
    if len(candidateList) > 0:
        stemCandidate = selectLongestInLexicons(candidateList, nounLexicon)
        if stemCandidate:
            newToken = stemCandidate
        else:
            newToken = selectShortest(candidateList)
        stemCandidate = newToken
    else:
        newToken = stemCandidate

    if newToken in nounLexicon:
        return getStemmedNoun(newToken), True

    candidateList = removePrefixes(word, prefixList)
    if len(candidateList) > 0:
        stemCandidate = selectLongestInLexicons(candidateList, nounLexicon)
        if stemCandidate:
            newToken = stemCandidate
        else:
            newToken = selectShortest(candidateList)
        stemCandidate = newToken
    else:
        newToken = stemCandidate

    if newToken in nounLexicon:
        return getStemmedNoun(newToken), True

    return "", False


def checkIfPrefixedVerb(word):
    candidateList = removePrefixes(word, ['در', 'بر', 'پر', 'باز',
                                          'ور', 'فرو', 'فرا', 'وا'])

    if len(candidateList) > 0:
        newToken = selectShortest(candidateList)
        if newToken:
            stemmed, flag = checkIfVerb(newToken)
            if flag:
                return stemmed, True

    return "", False


def checkIfNounTinSlam(word):
    candidateList = removePrefixes(word, prefixList)
    candidateList.add(word)

    if word.endswith("گان"):
        candidateList.add(word[:-3] + "ه")

    lengthiest = None
    for candidate in candidateList:
        if candidate in nounLexicon:
            if lengthiest is None or len(candidate) > len(lengthiest):
                lengthiest = candidate
    if lengthiest is not None:
        return lengthiest, True

    tempList = set({})
    for candidate in candidateList:
        tempList |= removePostfixes(candidate, postfixList)
    candidateList |= tempList

    lengthiest = None
    for candidate in candidateList:
        if candidate in nounLexicon:
            if lengthiest is None or len(candidate) > len(lengthiest):
                lengthiest = candidate
    if lengthiest is not None:
        return lengthiest, True

    tempList = set({})
    for candidate in candidateList:
        tempList |= removePostfixes(candidate, ["م", "ت", "ش", "یم", "یت", "یش",
                                                "یتان", "یشان", "یمان",
                                                "مان", "تان", "شان", "ان"])
    candidateList |= tempList

    lengthiest = None
    for candidate in candidateList:
        if candidate in nounLexicon:
            if lengthiest is None or len(candidate) > len(lengthiest):
                lengthiest = candidate
    if lengthiest is not None:
        return lengthiest, True

    tempList = set({})
    for candidate in candidateList:
        tempList |= removePostfixes(candidate, ["ها", "ات", "ون",
                                                "ان", "های", "ین"])
    candidateList |= tempList

    lengthiest = None
    for candidate in candidateList:
        if candidate in nounLexicon:
            if lengthiest is None or len(candidate) > len(lengthiest):
                lengthiest = candidate
    if lengthiest is not None:
        return lengthiest, True

    return "", False


def stem(word):
    notInNouns = True

    if word in nounLexicon:     # in dic
        notInNouns = False
        temp = getStemmedNoun(word)
        if temp != word:
            return getStemmedNoun(word)
    elif word in verbLexicon:  # past to present
        if word in verbP2F:
            return verbP2F[word]
        else:
            return word    # if present, itself

    stemmed, flag = checkIfVerb(word)
    if flag:
        return stemmed

    stemmed, flag = checkIfNounTinSlam(word)
    if flag:
        return stemmed

    stemmed, flag = checkIfPrefixedVerb(word)
    if flag:
        return stemmed

    # if notInNouns:
    #     print(word)
    return word


loadFiles()

# print(stem("می‌روم"))
# print(stem("گفتند"))
# print(stem("می‌خواهید"))
# print(stem("رفته است"))
# print(stem("شوند"))
# print(stem("درختان"))
# print(stem("کتابم"))
# print(stem("عادلانه‌ترین"))
# print(stem("جعبه‌ای"))
# print(stem("خانه‌هاهایمان"))
#
# if "خانه‌ها" in nounLexicon:
#     print("Why =|")

# print(stem("معتقد"))
# print(stem("بیشتر"))
# print(stem("بیشتر"))
# print(stem("بیشتر"))
# print(stem("بیشتر"))
# print(stem("بیشتر"))
# print(stem("است"))
# print(stem("وقت"))
# print(stem("کتب"))
# print(stem("مطالب"))
# print(stem("ارقام"))
# print("--------------------------")
# print(stem("داشتم‌می‌رفتم"))
# print(stem("نخواهم‌رفت"))
# print(stem("بروم"))
# print(stem("خواهد رفت"))
# print(stem("نخواهد رفت"))
# print(stem("رفتن"))
# print(stem("نرفت"))
# print(stem("برفت"))
# print("--------------------------")
# print(stem("کتابهایمان"))
# print(stem("پرندگان"))
# print(stem("کفتران"))
# print(stem("سگ ها"))
# print(stem("عالمان"))
# print(stem("علوم"))
# print(stem("روحانیون"))
# print("--------------------------")
# print(stem("برداشت"))
# print(stem("برداشته بود"))
# print(stem("برداشته است"))
# for item in verbLexicon:
#     print(item)

# list = []
# for item in nounLexicon:
# if item == "وق":
#     continue  # (.,. )
# list.append(item.strip())

# list.append('کتب')

# list = []
# for item in verbLexicon:
#     list.append(item.strip())

# list.append("است")
# list.append("هست")

# with open('Resources/Stemmer/Modified/verb_lexicon.pickle', 'wb') as handle:
#     pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)

# nounLexicon.append("امثال")
# nounLexicon.append("مثال")
# nounLexicon.append("اقدام")
# nounLexicon.append("چماقدار")
# nounLexicon.append("نماینده")
# nounLexicon.append("اصولگرا")
# nounLexicon.append("کتب")

# with open('Resources/Stemmer/Modified/noun_lexicon.pickle', 'wb') as handle:
#     pickle.dump(nounLexicon, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('Resources/Stemmer/Modified/noun_lexicon.pickle', 'wb') as handle:
#     pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)

# irregularNouns['امثال'] = 'مثال'
# with open('Resources/Stemmer/Modified/irregular_nouns.pickle', 'wb') as handle:
#     pickle.dump(irregularNouns, handle, protocol=pickle.HIGHEST_PROTOCOL)

# list = []
# list.append({})
# list.append({})
#
# for item in verbTenseMap[0]:
#     list[0][item.strip()] = verbTenseMap[0][item.strip()]
#
# for item in verbTenseMap[1]:
#     list[1][item.strip()] = verbTenseMap[1][item.strip()]
#
# with open('Resources/Stemmer/Modified/verb_tense_map.pickle', 'wb') as handle:
#     pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)

# print(verbTenseMap[0]['گذشت'])
