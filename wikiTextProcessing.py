import re
from collections import defaultdict
from nltk import PorterStemmer
from Stemmer import Stemmer
# from stemming import porter2 as stemming_porter2
from nltk.stem import WordNetLemmatizer

from nltk.corpus import stopwords as nltk_stopwords

import string

#stemmer = Port()
with open('stopwords.txt', 'r') as file :
    stopwords = file.read().split('\n')

with open('urlstopwords.txt', 'r') as file :
    url_stopwords = file.read().split('\n')

stopwords = set(stopwords)
url_stopwords = set(url_stopwords)

stemmed_dict = dict()

def checkIfEnglish(s):
    '''
        Checks if it is english character or not
    '''
    try:
        s = s.encode(encoding='utf-8')
        s = s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def cleanData(s,lowercase=False):

    """
       Function : 1. Lowers the case if not lowercase
                  2. Tokenisation
    """
    if lowercase == False:
        s = s.lower()

    return tokenisation(s)

def tokenisation(s):

    tokens = re.findall("\d+|[\w]+",s)
    #for i in range(len(tokens)):
    #   tokens[i] = tokens[i].encode('utf-8')

    return tokens

def removeUgly(s):

    """
        Input = words list
        Function = in each word it checks for numbers, punctuations and non-english chars and removes such numbers if found
    """
    newlist = []
    for word in s:
        temp = ''
        for ch in word:
            if ch in set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                continue
            if ch in set(list(string.punctuation) + ["\n", "\t", " "]):
                temp = ' '
                continue
            temp += ch

        if checkIfEnglish(temp):
            newlist.append(temp)

    return newlist

def removeStopWords(s):

    """
        Input = Words List
        Function = Checks for any stop words and removes it
    """

    newlist = []
    # URL stop words for much better indexing (removing shitty repetitive words)
    # stem the stop word
    for word in s:
        word = word.strip()
        if word in stopwords:
            continue
        if word in url_stopwords:
            continue
        if len(word) < 3:
            continue

        newlist.append(word)

    return newlist

def stemming(tokens):

    """
        Input = Tokens after tokenisation and removing stop words
        Function = Use stemmer to identify the root word
    """

    newlist = []

    for s in tokens:
        if s in stemmed_dict:
            str = stemmed_dict[s]
        else:
            str = Stemmer('english').stemWord(s)
            stemmed_dict[s] = str

        #if str not in newlist:
        newlist.append(stemmed_dict[s])

    return newlist

def makefreqList(s):

    dictionary = {}

    for word in s:
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    return dictionary
