import os
import re

def countwords(filepath):
    W=0
    with open (filepath,'r') as infile:
        lines = infile.readlines()
        for line in lines:
            if line[:3]=="<w>":
                W+=1
    return W

def printwordscount(fileslist):
    with open ('words_count.txt','w',encoding='utf-8') as outfile:
        for i in range(len(fileslist)):
            outfile.write(fileslist[i][1]+'\t'+str(countwords(fileslist[i][0]))+'\n')

def makefileslist(folderpath):
    outlist=[]
    filenames=os.listdir(folderpath)
    for filename in filenames:
        outlist.append([folderpath+os.sep+filename,filename])
    return outlist

def getmeta(filepath):
    outstr=""
    with open (filepath,'r') as infile:
        lines = infile.readlines()
        for line in lines:
            if line[:5]=="<meta" and re.search('author',line):
                outstr+=re.search('content="(.*?)"',line).group(1)
        outstr+=","
        for line in lines:
            if line[:5]=="<meta" and re.search('created',line):
                outstr+=re.search('content="(.*?)"',line).group(1)
    return outstr
        

def makecsv(fileslist):
    with open ('metadata.csv','w',encoding='utf-8') as outcsv:
        outcsv.write("Название файла,Автор,Дата создания текста\n")
        for i in range(len(fileslist)):
            outcsv.write(fileslist[i][1]+','+getmeta(fileslist[i][0])+'\n')

def makebigrams(fileslist):
    with open ('bigrams.txt','w',encoding='utf-8') as bigramstxt:
        for i in range(len(fileslist)):
            with open (fileslist[i][0],'r') as infile:
                sentencesarr=[]
                lines = infile.readlines()
                for line in lines:
                    if re.search('<se>',line):
                        sentencesarr.append([])
                    if line[:3]=="<w>":
                        sentencesarr[len(sentencesarr)-1].append(line)
                for sentence in sentencesarr:
                    sentencestr=""
                    for line in sentence:
                        sentencestr+=re.sub(r'<.?w>|</se>|\n|<.p>|</ana>|<ana.*?>| ','',line)
                        sentencestr+=' '
                    buffarr=[]
                    prevA=False
                    for line in sentence:
                        if re.search('A=',line) and re.search('gen',line) and not prevA:
                            buffarr.append(re.search('</ana>(.*?)</w>',line).group(1))
                            prevA=True
                        elif re.search('S,',line) and re.search('gen',line) and prevA:
                            buffarr.append(re.search('</ana>(.*?)</w>',line).group(1))
                            bigramstxt.write(buffarr[0]+' '+buffarr[1]+'\t'+sentencestr+'\n')
                            buffarr.pop()
                            buffarr.pop()
                            prevA=False
                        else:
                            prevA=False
                            if len(buffarr)>0:
                                buffarr.pop()

def main():
    flist=makefileslist('news')
    printwordscount(flist)
    makecsv(flist)
    makebigrams(flist)

main()
