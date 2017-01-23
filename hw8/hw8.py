import random
import re

def getdict (filepath):
    dic = {}
    with open(filepath, 'r', encoding='utf-8') as csv:
        rows = csv.readlines()
        for row in rows:
            rowvals = re.split(';|,|\n',row.replace(' ',''))
            if len(rowvals) == 2:
                dic[rowvals[0]] = rowvals[1]
            else:
                continue
    return dic

def orderresponses(correctfile,incorrectfile):
    responses = {}
    responses["Correct"] = []
    with open(correctfile, 'r', encoding='utf-8') as responsefile:
        lineresponses = responsefile.readlines()
        for response in lineresponses:
            if len(response) > 1:
                responses["Correct"].append(response)
    responses["Incorrect"] = []
    with open(incorrectfile, 'r', encoding='utf-8') as responsefile:
        lineresponses = responsefile.readlines()
        for response in lineresponses:
            if len(response) > 1:
                responses["Incorrect"].append(response)
    return responses


def riddle (dictname,orderedresponses):
    words = list(dictname.values())
    hints = list(dictname.keys())
    currenthint = random.choice(hints)
    while True:
        option = input(currenthint+' ')
        if dictname[currenthint] == option:
            print(random.choice(orderedresponses["Correct"]))
            break
        else:
            print(random.choice(orderedresponses["Incorrect"]))

riddle(getdict("in.csv"),orderresponses("correct.txt","incorrect.txt"))
