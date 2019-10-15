#from itertools import imap
from builtins import map
from operator import itemgetter
import heapq
import glob
from os import listdir
import os
from os.path import isfile, join

def mergeFiles(initDir, mergedDir, fileName, batchSize):

    #print('Merging Started \n')
    mypath = initDir #'./files/'
    files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    #xfiles = glob.glob("./files/*")
    #print(xfiles)
    #print(files)
    no_groups = len(files)/batchSize
    if type(no_groups) == float:
        no_groups = int(no_groups) + 1

    no_groups = 0
    #print(no_groups)
    while(len(files) > 1):
        i = 0
        #print(len(files))
        while(i < len(files)):

            no_groups = no_groups + 1
            opFiles = []

            for file in range(i,i+batchSize):
                #print('Files being added' + str(file))
                    #print(files)
                if file < len(files):
                    opFiles.append(open(files[file]))

                    #print("DONE WITH FILE WRINTING")

                    #for line in opFiles[0]:
                    #print(extract_comp(line))

            with open(mergedDir+"index"+fileName+str(no_groups), 'w') as dest:

                decorated = [((line.split(":",1)[0], line) for line in f) for f in opFiles]
                merged = heapq.merge(*decorated)
                undecorated = list(map(itemgetter(-1), merged))
                #print(undecorated)
                dest.writelines(undecorated)

                #f.close()
            for file in range(i,i+batchSize):
                if file < len(files):
                    os.remove(files[file])
            #print('Value of i : ' +str(i) )
            i = i + batchSize

            #print("Processing Batch -- " + str(no_groups))

        files = glob.glob(mergedDir+ "/*")
        #print('-------------------')
        #rint(len(files))
        #print('===================')


def merge1000Files(initDir, mergedDir, fileName, batchSize):

    mypath = initDir #'./files/'
    files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    i = 0
    opFiles = []

    for file in range(i,i+batchSize):
        #print('Files being added' + str(file))
        #print(files)
        if file < len(files):
            opFiles.append(open(files[file]))

    with open(mergedDir+"index"+fileName, 'w') as dest:

        decorated = [((line.split(":",1)[0], line) for line in f) for f in opFiles]
        merged = heapq.merge(*decorated)
        undecorated = list(map(itemgetter(-1), merged))
        #print(undecorated)
        dest.writelines(undecorated)


def mergeSimilarWords(path_to_index, indexfile, mergedDir):

    filenames = glob.glob(mergedDir + "*")
    final_index_file = indexfile
    f = open(filenames[0])

    offset_fileName = './offset.txt'
    offset_filepath = os.path.join(path_to_index, offset_fileName)
    offset_file = open(offset_filepath,'w')

    line = f.readline()

    if line :

        line = line.rstrip()
        prev_key = line.split(":",1)[0]
        offset_file.write(str(final_index_file.tell())+"\n")

        final_index_file.write(line)


    while True:

        line = f.readline()
        if not line:
            break
        line = line.rstrip()
        line_tokens = line.split(":",1)
        new_key = line_tokens[0]
        value = line_tokens[1]

        if(prev_key == new_key):
            final_index_file.write("|"+value)
        else:
            offset_file.write(str(final_index_file.tell())+"\n")
            final_index_file.write("\n"+line)

        prev_key = new_key

    offset_file.close()
    f.close()
