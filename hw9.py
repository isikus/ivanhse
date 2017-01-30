import re

def getarray(filename):
    wordarr=[]
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            linewords=line.split()
            for word in linewords:
                wordarr.append(cleanword(word))
    return wordarr

def cleanword(word):
    word=word.lower()
    falsechars = []
    for i in range(len(word)):
        if re.search("[a-яё]",word[i]) == None:
            falsechars.append(word[i])
    for char in falsechars:
        word = word.replace(char,"")
    return word

def searchforms(cleanedarray):
    for word in cleanedarray:
        if re.match("си(жу|ди(шь|м|те?)?|де(л[аои]?|в(ш(ая|е(му?|е|го|й)|ую|и(й|х|е|ми?)?))?|ть)|дя(т|щ(ая|е(му?|е|го|й)|ую|и(й|х|е|ми?)))?)\Z",word) != None:
                print(word)

searchforms(getarray("gulag.txt"))
    
