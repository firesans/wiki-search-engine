import re
from collections import defaultdict
from wikiTextProcessing import *
import string

INFOBOX_INDICATOR = '{{Infobox '
EXTERNAL_LINKS_INDICATOR = '==External links=='
CATEGORY_LINKS_INDICATOR = '[[Category:'
REFERENCES_INDICATOR = '==References=='

indexString = {}

def categoriseFieldData(linesd):

    infobox_data = []
    textbox_data = []
    category_data = []
    external_links = []
    reference_data = []

    #print('---------------------------------------------------------------------------------')
    #print(str(lines))
    #print(lines)
    lines = linesd.split('\n')
    #print(lines)
    #print(lines[3])

    flagtext = 1
    # pdb.set_trace()
    #for i in xrange(len(lines)):
    i = 0
    while 1:
        #print(i)
        if i >= len(lines)-1:
            break

        if INFOBOX_INDICATOR in lines[i]:
            flag = 0
            temp = lines[i].split(INFOBOX_INDICATOR)[1:]
            infobox_data.extend(temp)
            while True:
                if '{{' in lines[i]:
                    flag += lines[i].count('{{')
                if '}}' in lines[i]:
                    flag -= lines[i].count('}}')
                if flag <= 0:
                    break
                i += 1
                try:
                    infobox_data.append(lines[i])
                except:
                    break

        elif flagtext:
            if CATEGORY_LINKS_INDICATOR in lines[i] or REFERENCES_INDICATOR in lines[i] or EXTERNAL_LINKS_INDICATOR in lines[i]:
                flagtext = 0
            textbox_data.extend(lines[i].split())
            if REFERENCES_INDICATOR in lines[i]:
                #print("encounteref")
                while 1:
                    if i+1 >= len(lines) or lines[i+1].startswith("=") or lines[i+1].startswith("["):
                                #print("left ref")
                        break
                    else:
                        i = i + 1
                        reference_data.append(lines[i])



        #elif REFERENCES_INDICATOR in lines[i]:
        #    print("encountered references")

        elif CATEGORY_LINKS_INDICATOR in lines[i]:
            line = lines[i].split(CATEGORY_LINKS_INDICATOR)
            if len(line)>1:
                category_data.extend(line[1:-1])
                temp = line[-1].split(']]')
                category_data.append(temp[0])


        i = i +1
    #   pdb.set_trace()

    #print(reference_data)

    return infobox_data, textbox_data, category_data, external_links, reference_data

def dataProcessing(data):

    wordList = cleanData(str(data))
    #self.lines = []
    wordList = removeUgly(wordList)
    #val = removePunctuations(val)
    wordList = removeStopWords(wordList)
    wordList = stemming(wordList)

    dictlist = makefreqList(wordList)

    return dictlist


def makeFreqString(data1, data2, data3, data4, data5, data6):

    #indexString = {}
    addKeystoList(data1, 't')
    addKeystoList(data2, 'i')
    addKeystoList(data3, 'b')
    addKeystoList(data4, 'c')
    addKeystoList(data5, 'l')
    addKeystoList(data6, 'r')

    return indexString

def addKeystoList(data, ch):

    for k in data:
        try:
            indexString[k] += ch+str(data[k])
        except:
            indexString[k] = ch+str(data[k])
