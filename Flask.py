import os

from flask import Flask, render_template, request, redirect
import math
import random
from FileManager import readFile
from QueryFormatter import extractSpecialOperators
from QueryFormatter import convertToPostingsLists
from SearchEngine import loadInvertedIndex
from SearchEngine import constructInvertedIndex
from SearchEngine import query
from SearchEngine import getDictionary
from Laws import showZipf
from Laws import showHeap
from News import newsList
from News import formatTime

app = Flask(__name__)
newsId = 0
searchQuery = ""
feelingLucky = False
results = []
newsCount = 0
pageNumber = 1
resultsPerPage = 10


def getTime(news):
    return formatTime(news['time'])


def getScore(news):
    return 1 / news['score']


def sortByTime():
    results.sort(key=getTime)


def sortByRelevancy():
    results.sort(key=getScore)   # increasing sort


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def indexPage():
    global searchQuery, feelingLucky
    if request.method == "POST":
        if request.form['action'] == "feelingLucky":
            feelingLucky = True
        searchQuery = request.form['search bar']
        return redirect("/results.html")
    return render_template('index.html')


@app.route("/results.html", methods=['GET', 'POST'])
def resultPage():
    global newsId, pageNumber, results, newsCount, feelingLucky, searchQuery
    if request.method == "POST":
        idBox = request.form["idBox"]
        if idBox[0] == 'p':
            pageNumber = int(idBox[1:])
            pageNumber = max(1, min(math.ceil(newsCount / resultsPerPage), pageNumber))
        elif idBox.startswith("sort_"):
            if idBox == "sort_time":
                sortByTime()
            else:
                sortByRelevancy()
        else:
            newsId = int(idBox)
            return redirect("/news.html")
    else:
        pageNumber = 1
        searchQuery, category, source = extractSpecialOperators(searchQuery)
        lists, tokens = convertToPostingsLists(searchQuery, 0, isRankedBased)
        results = query(lists, tokens, isRankedBased)
        newsCount = results.__len__()
        if feelingLucky:
            feelingLucky = False
            if newsCount != 0:
                newsId = newsList[random.randint(0, newsCount - 1)].id
                return redirect("/news.html")
    return render_template('results.html', newsList=results,
                           pageNumber=pageNumber,
                           resultsPerPage=resultsPerPage,
                           forEndIndex=min(pageNumber * resultsPerPage, newsCount),
                           pageBegin=max(1, pageNumber - 3),
                           pageEnd=min(math.ceil(newsCount / resultsPerPage), pageNumber + 3))


@app.route("/news.html")
def newsPage():
    return render_template('news.html', news=newsList[newsId].structuredFormatNewsPage())


if __name__ == "__main__":
    # readFile("data/IR-F19-Project01-Input-2k.xlsx")
    readFile("data/IR-F19-Project02-14k.xlsx")
    isRankedBased = True
    # constructInvertedIndex()
    loadInvertedIndex(isRankedBased)
    # showZipf(getDictionary())
    # showHeap()
    os.system("start chrome http://127.0.0.1:31807")
    app.run(host="127.0.0.1", port=31807)
