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
        if ord(word[i]) < 97 or ord(word[i]) > 123:
            falsechars.append(word[i])
    for char in falsechars:
        word = word.replace(char,"")
    return word

def get_value_and_percentage(arrayname, minlength):
    unWords = 0
    unWordsByLength = 0
    for word in arrayname:
        if word[:2] == "un":
            unWords = unWords + 1
            if len(word) > minlength:
                unWordsByLength = unWordsByLength + 1
    print("Слов с приставкой un-: ",unWords)
    if unWords > 0:
        print("Процент слов с количеством символов больще ", minlength,": ",unWordsByLength/unWords*100)
    else:
        print("Процент слов с количеством символов больще ", minlength,": ",0)

fpath="Austen Jane.txt"
inplength = int(input("В искомых словах символов должно быть больше чем: "))
print("Анализируем файл ",fpath,"...")
get_value_and_percentage(getarray(fpath), inplength)
