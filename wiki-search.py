import string
import sys
import os
import re
import time
from wikiTextProcessing import *
from fieldExtraction import *
from collections import defaultdict

def LinearSearch(queryWordList, indexFile):

    searchList = set()
    searchList.add(-1)
    #searchList = set(list(range(1,28700))
    file = open(indexFile, 'r')

    flagsum = len(queryWordList)

    while True:
        line = file.readline()
        if flagsum == 0 or (line == None):
            break

        ind = line.split(":",1)[0]

        if ind in queryWordList:

            value = line.split(":",1)[1]

            value = value[:-1]
            value = value.split("|")
            docIDlist = []
            for val in value:
                docIDlist.append(val.split(":",1)[0])

            docIDlist = set(docIDlist)

            if searchList == {-1}:
                if len(docIDlist) != 0:
                    searchList = docIDlist

            else:
                temp = searchList & docIDlist
                if len(temp) == 0:
                    flag = True
                else:
                    searchList = temp

            flagsum = flagsum - 1

    return searchList

def queryProcessing(queryText):

    wordList = cleanData(str(queryText))
    wordList = removeUgly(wordList)
    wordList = removeStopWords(wordList)
    wordList = stemming(wordList)

    return wordList

def fieldQueryProcessing(queryText):

    queryDict = dict()
    queryText = queryText.split(" ")

    for queryWord in queryText:
        queryW = queryWord.strip().split(":",1)[1].lower()
        queryType = queryWord.strip().split(":",1)[0]
        queryW = list([queryW])
        #print(type(queryW))
        #print(queryW)
        w = removeUgly(queryW)
        #print(w)
        w = removeStopWords(w)
        #print(w)
        w = stemming(w)
        #print(w)
        w = "".join(w)
        val = queryType[0]
        if w in queryDict:
            queryDict[w].append(val)
        else:
            queryDict[w] = [val]

    return queryDict

def valueProcessing(list,queryT):

    #valueList = []
    valueSet = set({-1})

    for q in queryT:
        valueList = []
        for postList in list:
            postListV = postList.split(":",1)[1]
            postListID = postList.split(":",1)[0]

            regexString = r'{0}'.format(q)
            rex = re.compile(regexString)

            if rex.search(postListV):
                valueList.append(postListID)

            #print(valueList)
        #print(q)
        #print(valueList)
        if len(valueList) == 0:
            valueSet = valueSet

        else:
            #print(valueSet)
            if valueSet == {-1}:
                valueSet = set(valueList)
            else:
                temp = valueSet & set(valueList)
                if len(temp) == 0:
                    flag = True
                else:
                    valueSet = temp
        #print(valueSet)

    return valueSet

def LinearFieldSearch(fieldQueries,indexFile):

    searchList = set()
    searchList.add(-1)
    #searchList = set(list(range(1,28700))
    file = open(indexFile, 'r')

    flagsum = len(fieldQueries)
    flagi = False
    while True:
        #print("Reading--")
        line = file.readline()

        if flagsum == 0 or (line == None):
            break

        ind = line.split(":",1)[0]

        if ind in fieldQueries:
            #print(ind)

            value = line.split(":",1)[1]
            value = value[:-1]
            value = value.split("|")
            #print(fieldQueries[ind])
            fieldValues = valueProcessing(value,fieldQueries[ind])
            #print(fieldValues)

            docIDlist = []
            for val in fieldValues:
                docIDlist.append(val)

            docIDlist = set(docIDlist)

            if searchList == {-1}:
                if len(docIDlist) == 0:
                    flag = True
                else:
                    searchList = docIDlist

            else:
                temp = searchList & docIDlist
                searchList = temp

            flagsum = flagsum - 1

    return searchList

def main_query_processing(path_to_index, arguments):

    indexFile = path_to_index
    titlelistName = './titles.txt'

    regex_FIELDS = re.compile(r'(title|body|infobox|category|ref):')
    if regex_FIELDS.search(arguments):
        #print("Entered the field queries section")
        fieldQueries = fieldQueryProcessing(arguments)
        #print(fieldQueries)
        #for k,v in fieldQueries.items():
        #    print (k,v)

        searchSet = LinearFieldSearch(fieldQueries,indexFile)
        #print(searchSet)

    else:
        queryWords = set(queryProcessing(arguments))
        searchSet = LinearSearch(queryWords,indexFile)

    #####################################################
    titlefile = open(titlelistName,"r")
    titles = []
    line = titlefile.readline()
    titles.append(line)
    while line:
        line = titlefile.readline()
        titles.append(line)
    titlefile.close()
    #####################################################

    resultDocuments = []
    if searchSet == set():
        resultDocuments.append("Sorry,No Results!")
    else:
        for docID in searchSet:
            resultDocuments.append(titles[int(docID)-1])

    return resultDocuments

def printResults(listOfTitleResults):

    if len(listOfTitleResults) != 0:
        count = 0
        print("Search Results: \n")
        for title in listOfTitleResults:
            #if count >= 10:
            #    break
            count = count + 1
            print(title)
    else:
        print("Sorry!, no results.")


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


def search(path_to_index, queries):
    '''Write your code here'''
    results = []
    for q in queries:
        start = time.time()
        curr_result = main_query_processing(path_to_index,q)
        end = time.time()
        print("Search Time "+"for query : "+q)
        print(end-start)
        #print("\n")
        results.append(curr_result)

    return results

def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)

if __name__ == '__main__':
    main()
