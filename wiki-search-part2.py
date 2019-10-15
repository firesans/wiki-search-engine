import string
import sys
import os
import re
import time
import math
from wikiTextProcessing import *
from fieldExtraction import *
from collections import defaultdict
import operator

field_weights = {'t':5,'b':3,'c':1,'i':2,'r':1}

def BinarySearch_offsetFile(file_desc, low, high, offset_arr, word):

    while high >= low:

        mid = int((low+high)/2)
        file_desc.seek(offset_arr[mid]+1)
        #file_desc.seek(2)
        line = file_desc.readline()
        #print(p)
        #print(offset_arr[mid])
        #line = file_desc.readline()
        #print(line)
        #line = p
        line = line.rstrip("\n")
        keyword = line.split(":",1)[0]
        val = line.split(":",1)[1]

        if word == keyword:
            return val
        elif word > keyword:
            low = mid+1
        elif word < keyword:
            high = mid-1

    return []

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

def calcDocFreqWord(strVal):

    strVal = strVal.split("|")
    if strVal == "":
        return 0
    return len(strVal)

def collectPagesQueries(index_file_fd, offset, queries):

    listofFiles = defaultdict()
    df = defaultdict()

    for term in queries:
        keyString = BinarySearch_offsetFile(index_file_fd,0,len(offset)-1,offset,term)
        listofFiles[term] = keyString
        df_word = calcDocFreqWord(keyString)
        df[term] = df_word

    return listofFiles, df

def rankingDocs(queryPages, docFreq, num_Files):

    idf_word = defaultdict()
    doc_score = defaultdict()

    # Compute the IDF for each word
    for term in docFreq:
        idf_word[term] = math.log((float(num_Files)/(float(docFreq[term]) + 1)))
    #print(idf_word)

    for query in queryPages:

        strVal = queryPages[query]
        pages = strVal.split("|")
        for page in pages:

            score = 0
            pageID = page.split(":",1)[0]
            pagestr = page.split(":",1)[1]
            tfield = re.findall('[a-z]+',pagestr)
            tfreq = re.findall('[0-9]+',pagestr)
            termdict = {k:float(v) for k,v in zip(tfield, tfreq)}
            #print(termdict)

            for field in termdict:
                score += math.log(1+float(termdict[field])) * idf_word[query] * field_weights[field]

            if pageID in doc_score:
                doc_score[pageID] += score
            else:
                doc_score[pageID] = score
            #print(doc_score[pageID])

    return doc_score

def rankingDocs_field(queryPages, docFreq, fieldQueries, num_Files):

    idf_word = defaultdict()
    doc_score = defaultdict()

    # Compute the IDF for each word
    for term in docFreq:
        idf_word[term] = math.log((float(num_Files)/(float(docFreq[term]) + 1)))

    for query in queryPages:

        strVal = queryPages[query]
        pages = strVal.split("|")

        for page in pages:

            score = 0
            pageID = page.split(":",1)[0]
            pagestr = page.split(":",1)[1]

            tfield = re.findall('[a-z]+',pagestr)
            tfreq = re.findall('[0-9]+',pagestr)

            termdict = {k:int(v) for k,v in zip(tfield, tfreq)}

            for f in fieldQueries[query]:
                if f in termdict:
                    score = score + (math.log(1+termdict[f]) * idf_word[query] * field_weights[f])
                else:
                    score = score

            if pageID in doc_score:
                doc_score[pageID] += score
            else:
                doc_score[pageID] = score

    return doc_score

def best10(docScores):

    #print(docScores)
    best10dict = defaultdict()

    res = sorted(docScores.items(), key= lambda x:x[1], reverse=True)
    #print(res[0:10])
    keysList = []
    #keysList = {key for key,value in res[0:10]}
    #keysList = list(res.keys())[0:10]
    #print(keysList)
    for key in res[0:10]:
        ide,sco = key 
        keysList.append(ide)

    #print(best10dict)
    return keysList

def getTitles(firstDocs, titleoffset, titlefile):

    resultTitles = []

    for doc in firstDocs:
        titlefile.seek(titleoffset[int(doc)-1])
        #titlefile.seek(26)
        #file_desc.seek(2)
        line = titlefile.readline()
        resultTitles.append(line.rstrip("\n"))
    return resultTitles

def main_search_offset(path_to_index, offset_arr, indexFD, arguments, titleoffset, titlefile, numfiles):

    #Query Processing
    regex_FIELDS = re.compile(r'(title|body|infobox|category|ref):')
    if regex_FIELDS.search(arguments):
        #print("Entered the field queries section")
        fieldQueries = fieldQueryProcessing(arguments)
        #print(fieldQueries)
        queryPages, docFreq = collectPagesQueries(indexFD, offset_arr, fieldQueries)
        doc_ranked_score = rankingDocs_field(queryPages, docFreq, fieldQueries, numfiles)
        resultDocs = best10(doc_ranked_score)
        resDocumentTitles = getTitles(resultDocs, titleoffset, titlefile)
        #searchSet = LinearFieldSearch(fieldQueries,indexFile)
        #print(searchSet)

    else:
        queryWords = set(queryProcessing(arguments))
        queryPages, docFreq = collectPagesQueries(indexFD, offset_arr, queryWords)
        doc_ranked_score = rankingDocs(queryPages,docFreq, numfiles)
        resultDocs = best10(doc_ranked_score)
        resDocumentTitles = getTitles(resultDocs, titleoffset, titlefile)
        #print(resDocumentTitles)
        #searchSet = Searchfunc(queryWords,indexFile)
    return resDocumentTitles


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries

def printResults(listOfTitleResults):

    if len(listOfTitleResults) != 0:
        count = 0
        print("Search Results: \n")
        for title in listOfTitleResults:
            #if count >= 10:
            #    break
            count = count + 1
            print(str(count) + ". "+ title)
    else:
        print("Sorry!, no results.")

def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


def search(path_to_index, offset, index_file_fd, query, titleoffset, num_Files):
    '''Write your code here'''

    #for q in queries:
    start = time.time()
    titlefile = open(path_to_index+'./titles.txt',"r")
    curr_result = main_search_offset(path_to_index, offset, index_file_fd, query, titleoffset, titlefile, num_Files)
    end = time.time()
    printResults(curr_result)
    #titlefile.close()
    print("\nSearch Time "+"for query : "+query)
    print(end-start)
    print("\n")
    #print("\n")
    #results.append(curr_result)
    titlefile.close()

def main():
    path_to_index = sys.argv[1]
    #testfile = sys.argv[2]
    #ath_to_output = sys.argv[3]

    file_num_path = os.path.join(path_to_index,'file_num.txt')
    with open(file_num_path,'r') as f:
        num_Files = int(f.read().strip())
    ##########################################################

    results = []
    titlelistName = os.path.join(path_to_index,'titles.txt')
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

    ######################################################
    #Read offset file
    offsetfileName = 'offset.txt'
    offsetfileName_path = os.path.join(path_to_index, offsetfileName)
    offsetfile = open(offsetfileName_path,"r")
    offset = []
    line = offsetfile.readline()
    offset.append(line)
    while line:
        line = offsetfile.readline().rstrip('\n')
        #print(line)
        if line != "":
            offset.append(int(line))
    offsetfile.close()
    ######################################################
    #Read Title offset file
    titleoffsetfileName = 'Titleoffset.txt'
    titleoffsetfileName_path = os.path.join(path_to_index, titleoffsetfileName)
    offsetfile = open(titleoffsetfileName_path,"r")
    titleoffset = []
    line = offsetfile.readline()
    titleoffset.append(line)
    while line:
        line = offsetfile.readline().rstrip('\n')
        #print(line)
        if line != "":
            titleoffset.append(int(line.strip()))
    offsetfile.close()

    #print(titleoffset[0])
    #print(titleoffset[1])

    ######################################################
    #Index File filedescriptor
    indexFileName = 'index.txt'
    indexFileName_path = os.path.join(path_to_index, indexFileName)
    index_file_fd = open(indexFileName_path,"r")
    ######################################################

    while(1):
        query = input("Enter the query\n")
        if(query == "exit"):
            break
        #queries = read_file(testfile)
        search(path_to_index, offset, index_file_fd, query, titleoffset, num_Files)
        #write_file(outputs, path_to_output)
        #printResults(outputs)



if __name__ == '__main__':
    main()
    #main_search_offset(sys.argv[1],'./offset.txt')

