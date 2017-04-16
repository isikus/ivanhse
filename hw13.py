import os
import re

def getfolders():
    folder = os.listdir()
    dirsdict = {}
    dirs = 0
    for entity in folder:
        if os.path.isdir(entity) and re.search(r'[a-zA-Z]',entity) and re.search(r'[а-яёА-ЯЁ]',entity):
            dirs += 1
            if entity not in dirsdict:
                print(entity)
    print()
    print (dirs,'directories total found.')

getfolders()
