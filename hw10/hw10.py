import re

def getcode(filename):
    with open (filename,'r',encoding='utf-8') as f:
        t=f.read()
        return re.search('ISO 639-3(.|\n)*?http:\/\/www-01\.sil\.org\/iso639-3\/documentation\.asp\?id=(...)',t).group(2)

def main():
    print(getcode('korean.html'))

main()
