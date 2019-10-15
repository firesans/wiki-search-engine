import re
from collections import defaultdict
from wikiTextProcessing import *
import string

INFOBOX_INDICATOR = '{{Infobox '
EXTERNAL_LINKS_INDICATOR = '==External links=='
CATEGORY_LINKS_INDICATOR = '[[Category:'
REFERENCES_INDICATOR = '==References=='

indexString = {}

def categoriseFieldData(lines):

    infobox_data = []
    textbox_data = []
    category_data = []
    external_links = []
    reference_data = []

    #print('---------------------------------------------------------------------------------')
    #print(str(lines))
    #print(lines)
    lines = lines.split('\n')
    #print(lines)
    #print(lines[3])
    i = 0
    #print(len(lines))
    #for i in range(len(lines)):
    while 1:
        #print(i)
        if (i>=len(lines)-1):
            break

        #''' ---INFOBOX--- '''
        if lines[i].startswith(INFOBOX_INDICATOR):
            #print('entered')
            line = lines[i].split(INFOBOX_INDICATOR)
            line = line[1:]
            infobox_data.extend(line)
            #print(line)

            while 1:
                if i+1 >= len(lines) or lines[i].endswith('}}'):
                    #print("left info")
                    break
                i = i + 1
                infobox_data.append(lines[i])
                #print(infobox_data)
                #print(lines[i])

        #''' ---CATEGORY--- '''

        elif lines[i].startswith(CATEGORY_LINKS_INDICATOR):
            line = lines[i].split(CATEGORY_LINKS_INDICATOR)
            line = line[1:]
            #line = line[:-2]
            category_data.append(line)

        elif lines[i].startswith('=='):
            if lines[i] == REFERENCES_INDICATOR:
                while 1:
                    if i+1 >= len(lines) or lines[i+1].startswith("=") or lines[i+1].startswith("["):
                        #print("left ref")
                        break
                    else:
                        i = i + 1
                        reference_data.append(lines[i])
            #if lines[i] == EXTERNAL_LINKS_INDICATOR:
            #    while 1:
            #        if i+1 >= len(lines) or lines[i+1].startswith("="):
            #            print("left ext")
            #            break
            #        i = i + 1
            #        external_links.append(lines[i])
            #
            #continue

        else:
            #print('entered')
            textbox_data.append(lines[i])

        #print(infobox_data)
        i = i + 1


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
