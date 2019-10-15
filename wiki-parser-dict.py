import sys
import timeit
import xml.sax
import time
from xml.sax import make_parser
from wikiTextProcessing import *
from fieldExtraction_new import *
from merge import *
import re
import os

#tokenisation_REGEX = re.compile("\d+|[\w]+")

class WikiParser(xml.sax.ContentHandler):

    def __init__(self):

        self.CurrentData=''
        self.titles = ''
        self.pages = 0
        self.text=''
        self.filename = None
        self.titleList = []

        self.time1 = 0
        self.time2 = 0
        self.Parsetime = 0
        self.Parsetime1 = 0
        self.MegaDocString = defaultdict()
        self.count = 10000
        self.files_path = None
        self.batch = 0

    def startElement(self,tag,attributes):
        self.CurrentData=tag

        if tag=='page':

            self.ide=[]
            self.text = ''
            self.titles = ''
            self.Parsetime1 = time.time()

    def characters(self,content):

        if self.CurrentData== "title":
            self.titles = content

        elif self.CurrentData=='id':
            self.ide.append(content)

        elif self.CurrentData=='text':
            self.text += content

    def endElement(self,tag):

        if tag == "page":

            print(self.count)
            self.Parsetime += time.time() - self.Parsetime1
            start = time.time()
            mylist=[]
            self.pages = self.pages + 1
            mylist.append(self.titles)
            self.titleList.append(self.titles)
            infobox_data, textbox_data, category_data, external_links, reference_data = categoriseFieldData(self.text)

            iD = self.ide[0]
            curr_path = os.getcwd()
            files_dir = curr_path+'/files/'
            fileName = files_dir+iD

            #self.filename = open(fileName,"w")

            title_data_list = dataProcessing(mylist)
            infobox_data_list = dataProcessing(infobox_data)
            textbox_data_list = dataProcessing(textbox_data)
            category_data_list = dataProcessing(category_data)
            external_links_list = dataProcessing(external_links)
            reference_data_list = dataProcessing(reference_data)

            docString = makeFreqString(title_data_list,infobox_data_list,textbox_data_list,category_data_list,external_links_list,reference_data_list)
            end = time.time()

            self.time1 += end - start

            start = time.time()

            #docStringkeys = sorted(docString.keys())
            docStringkeys = docString.keys()
            #print(doc  String)

            if self.count !=0:
                MegaDocStringkeys = self.MegaDocString.keys()
                for key in docStringkeys:
                    if key in MegaDocStringkeys:
                        self.MegaDocString[key] = self.MegaDocString[key] + "|" + str(self.pages)+":"+docString[key]
                    else:
                        self.MegaDocString[key] = str(self.pages)+":"+docString[key]

                self.count = self.count -1;

            if self.count <= 0:

                #if(self.batch == 1):
                #    for key in docStringkeys:
                #        self.filename.write(key+':'+str(self.pages)+':'+docString[key]+"\n")

                #else:
                fileName = files_dir+str(self.batch)
                self.filename = open(fileName,"w")
                self.count = 10000
                #print("Wrote in a file")

                for key in sorted(self.MegaDocString.keys()):
                    self.filename.write(key+':'+self.MegaDocString[key]+"\n")

                self.filename.close()
                self.batch = self.batch + 1
                self.MegaDocString.clear()

            #---------------------
            #for key in docStringkeys:
            #    self.filename.write(key+':'+str(self.pages)+':'+docString[key]+"\n")

            #self.filename.close()

            #self.count = self.count - 1

            #if self.count <= 1:

            #    merge1000Files(files_dir,self.files_path,str(self.batch),1000)
            #    self.count = 1000

            #    self.batch = self.batch + 1

            #    files = glob.glob('intermediate_files/*')
            #    for f in files:
            #    	os.remove(f)
            #----------------------
                #print("%s: %s" % (key, mydict[key]))


            indexString.clear()
            end = time.time()

            self.time2 += end - start

            #self.filename.write('{"id":'+self.ide+',"title":'+str(mylist)+',"text":'+str(self.lines)+'\n')
            self.titles=[]
            self.flag = 0
            self.text = ''
            #self.page_title=[]
            #self.ids.append(self.ide)

        #if tag == "id":
            #print(self.ide)
        self.CurrentData=''

def main():

    path_to_dump = sys.argv[1]
    path_to_index = sys.argv[2]

    #############################################
    #current_path = os.getcwd()
    #title_path = path_to_index +"titles.txt"
    title_path = os.path.join(path_to_index,'titles.txt')
    file_num_path = os.path.join(path_to_index,'file_num.txt')
    titleOffset_path = os.path.join(path_to_index,'Titleoffset.txt')

    intermediate_files_path = 'intermediate_files/'
    files_dir_path = 'files/'
    #os.mkdir(files_dir_path)

    merged_files_path = 'MergedFiles/'
    #os.mkdir(merged_files_path)

    files = glob.glob('MergedFiles/*')
    for f in files:
    	os.remove(f)
    files = glob.glob('files/*')
    for f in files:
    	os.remove(f)

    # ----PARSING OF XML DATA-------
    #############################################
    startTime = time.time()
    Handler = WikiParser()
    #Handler.filename = open("sample.txt","w")
    #os.mkdir('./ahah')
    Handler.files_path = files_dir_path
    xml.sax.parse(open(path_to_dump),Handler)
    #remaining files
    files = glob.glob('intermediate_files/*')
    for f in files:
        os.remove(f)

    print(Handler.pages)

    filenumber = open(file_num_path,"w")
    filenumber.write(str(Handler.pages))
    filenumber.close()

    if Handler.count >= 0:

        fileName = files_dir_path+str(Handler.batch)
        fileN = open(fileName,"w")

        for key in sorted(Handler.MegaDocString.keys()):
            fileN.write(key+':'+Handler.MegaDocString[key]+"\n")

        fileN.close()

    #Print titles in a file
    #############################################
    TitleList = Handler.titleList
    titleoffsetfd = open(titleOffset_path,'w')
    filename = open(title_path,"w")
    for val in TitleList:
        titleoffsetfd.write(str(filename.tell())+'\n')
        filename.write(val+"\n")
    filename.close()
    titleoffsetfd.close()
    #############################################

    print('Parsing Time: \n')
    #xml.sax.parse(source,wikihandler )              #XmlParsing
    stopTime = time.time()
    print(stopTime - startTime)
    #print(stop - start)
    start = time.time()
    indexName = open(path_to_index+'index.txt','w')

    mergeFiles(files_dir_path,merged_files_path,"_",1000)
    mergeSimilarWords(path_to_index, indexName, merged_files_path)

    stop = time.time()

    ##############################################
    ##############################################
    # TIME PRINTING

    print('Merging Time : \n')
    print(stop - start)
    print('Total Time \n')
    print(stop + stopTime - start - startTime)

    print('--------------------------')
    print('Only Parsing time: ' + str(Handler.Parsetime))
    print('Processing Time' + str(Handler.time1))
    print('Index Writing Time' + str(Handler.time2))

    #print "total number of pages",len(wikihandler.Pages)
    Handler.filename.close()

if __name__=='__main__':

    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    main()
