with open('aphor.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if len(line.split()) < 17:
            print (line)

resstr=""
aphors=0
with open('aphor.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        splitted = line.split()
        for word in splitted:
            if word[len(word)-1]=="." or word[len(word)-1]=="," or word[len(word)-1]=="?":
                word=word[:-1:]
            word=word.lower()
            if word=="ум":
                aphors=aphors+1
                if resstr!="":
                    resstr+=", "
                resstr+=splitted[len(splitted)-1]
                break
print('Цитат, содержащих слово "ум": '+str(aphors))
print(resstr)
print()

print("Введите слова:")
wordarr=[]
while True:
    i=input()
    if i=="":
        break
    wordarr.append(i)
with open('aphor.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for inpword in wordarr:
        print(inpword+":")
        printed=False
        inpword=inpword.lower()
        for line in lines:
            splitted = line.split()
            for word in splitted:
                if word[len(word)-1]=="." or word[len(word)-1]=="," or word[len(word)-1]=="?":
                    word=word[:-1:]
                word=word.lower()
                if word==inpword:
                    printed=True
                    print(line[:-1:])
                    break
        if not printed:
            print("Слово "+inpword+" в цитатах не найдено")
        print()
