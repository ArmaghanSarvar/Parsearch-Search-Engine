from Tokenizer import isSeparator
from Normalizer import normalize

newsList = []   # it is filled in FileManager
newsCounter = 0


class News:
    def __init__(self, time, title, source, abstract, keywords, content, thumbnail):
        global newsCounter
        self.id = newsCounter
        self.score = 0
        self.hasQueryTerm = False
        self.time = time
        self.title = title
        self.source = source
        self.abstract = str(abstract)
        self.keywords = keywords
        self.content = content
        self.thumbnail = thumbnail
        newsCounter += 1

    def pick_query_containing_phrases(self, tokens_to_be_bold):
        phrase = []
        normed = normalize(self.content).split()
        for i in range(0, len(normed)):
            if normed[i] in tokens_to_be_bold:
                temp = ""
                for j in range(-3, 3):
                    temp += (normed[min(len(normed) - 1, max(0, i+j))]) + " "
                phrase.append(temp)
                if len(phrase) > 4:
                    break
        return phrase

    def formatAbstract(self, tokens):      # make tokens bold
        string = self.abstract
        string += '<br>'
        for phrase in self.pick_query_containing_phrases(tokens):
            string += phrase + '...'
        for token in tokens:
            index = string.find(token)
            while index != -1:
                valid = False
                if index == 0 and isSeparator(string[index + len(token)]):
                    valid = True
                elif index + len(token) == len(string) and isSeparator(string[index - 1]):
                    valid = True
                elif isSeparator(string[index - 1]) and isSeparator(string[index + len(token)]):
                    valid = True
                if valid:
                    newString = "<strong>" + token + "</strong>"
                    string = string[:index] + newString + string[index + len(token):]
                    index += len(newString)
                index += 1
                index = string.find(token, index)
        return string

    def roundTime(self):
        return self.time[:-7]

    def structuredFormatResultsPage(self, tokens):
        return {
            'id': self.id,
            'title': self.title,
            'time': self.roundTime(),
            'score': self.score,
            'source': self.source,
            'thumbnail': self.thumbnail,
            'abstract': self.formatAbstract(tokens)
        }

    def structuredFormatNewsPage(self):
        return {
            'id': self.id,
            'title': self.title,
            'time': self.roundTime(),
            'score': self.score,
            'source': self.source,
            'thumbnail': self.thumbnail,
            'abstract': self.abstract,
            'keywords': str(self.keywords)[1:-1],
            'content': self.content
        }


def getMonthValue(string):
    if string == "January":
        return "01"
    elif string == "February":
        return "02"
    elif string == "March":
        return "03"
    elif string == "April":
        return "04"
    elif string == "May":
        return "05"
    elif string == "June":
        return "06"
    elif string == "July":
        return "07"
    elif string == "August":
        return "08"
    elif string == "September":
        return "09"
    elif string == "October":
        return "10"
    elif string == "November":
        return "11"
    elif string == "December":
        return "12"


def formatTime(string):
    time = ""
    tokens = string.split()
    time += tokens[2][:-1]
    time += getMonthValue(tokens[0])
    day = tokens[1][:-2]
    if len(day) < 2:
        day = "0" + day
    time += day
    time += tokens[3]
    return time


def setNewsList(value):
    global newsList, newsCounter
    newsList = value
    newsCounter = 0


def getNewsList():
    return newsList
